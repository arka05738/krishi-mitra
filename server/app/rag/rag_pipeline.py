"""
Offline RAG Advisory Pipeline for Indian Farmers.
Integrates ChromaStore vector retrieval, local Ollama llama3.2:3b synthesis,
strict zero-tech-leakage enforcement, and graceful offline fallback generation.
"""

import os
import re
import json
from typing import List, Optional, Generator, Dict, Any
import httpx
from pydantic import BaseModel, Field

from .chroma_store import ChromaStore, get_chroma_store
from .multilingual import get_language_directive, localize_fallback_advisory, INDIC_LANGUAGES


class AdvisoryResult(BaseModel):
    query: str
    crop_name: Optional[str] = None
    answer: str
    sources: List[str]
    urgency_level: str  # "Normal", "Advisory", "Urgent"
    helpline: str = "Kisan Call Centre: 1800-180-1551"


FARMER_SYSTEM_PROMPT = """You are Krishi Mitra, a trusted, practical agricultural advisory guide for Indian farmers.
Your mission is to provide clear, actionable, and safe farming guidance based strictly on authoritative ICAR, TNAU, IMD, and Soil Health Card practices.

STRICT COMMUNICATION RULES:
1. ZERO TECHNICAL LEAKAGE: Never mention artificial intelligence, AI, machine learning, neural networks, models, llama, LLMs, embeddings, vectors, ChromaDB, databases, servers, APIs, algorithms, tokens, pipelines, or any internal software/hardware systems. You are a knowledgeable agricultural expert, not a computer program.
2. FARMER-FACING LANGUAGE: Speak with warmth, respect, and simplicity. Use terms familiar to Indian farmers (Kharif, Rabi, Zaid, bigha, acre, neem cake, FYM, DAP, Urea, SSP, MOP).
3. EXACT PRODUCT NAMES & DOSAGES: Always give specific commercial chemical or fertilizer names, formulations, and application rates (e.g., "Mancozeb 75% WP @ 2.0 to 2.5 grams per liter of water" or "Neem-Coated Urea @ 45 kg per acre in split doses").
4. INTEGRATED MANAGEMENT & SAFETY: Prioritize sanitation, cultural methods, and bio-agents before chemical sprays. Include safety cautions (protective gear, morning/evening spraying).
5. MANDATORY HELPLINE: Always conclude your advice with:
"For immediate free telephonic guidance, contact the toll-free Kisan Call Centre helpline at 1800-180-1551 (6:00 AM to 10:00 PM)."
"""

FARMER_PROMPT_TEMPLATE = """Authoritative Agronomic Reference:
{retrieved_context}

Farmer Query / Situation:
{query}

{vision_context}

Please provide your practical advisory following this structure:
1. Diagnosis & Summary (1-2 clear sentences)
2. Action Steps & Exact Dosages (Cultural, Biological, Chemical with commercial product names)
3. Precautions & Safety
4. Kisan Call Centre Helpline: 1800-180-1551
"""

# Regex patterns for accidental technical jargon leaks
LEAKAGE_BLACKLIST_PATTERNS = [
    r"\b(ai|llm|llama3\.2|llama3?|rag|vector|vectors|embedding|embeddings|chromadb?|chroma|database|system prompts?|prompts?|token|tokens|pipeline|api|endpoint|models?|parameters?)\b",
    r"\b(neural network|language model|artificial intelligence|machine learning)\b",
    r"\b(context window|similarity score|retrieval store)\b",
    r"\b(?:(?:sampling|model)\s+temperature|(?:sampling_)?temperature\s*=\s*\d+\.?\d*|temperature\s*:\s*(?:0(?:\.\d+)?|1(?:\.\d+)?|2(?:\.0+)?)\b(?!\s*(?:°|deg|celsius|centigrade|\bc\b|\bf\b)))",
    r"\b(?:top_p|top_k)\s*(?:[:=]\s*\d+\.?\d*)?\b",
    r"\b(hugging\s*face|huggingface|vit|convolution(?:al)?|backpropagation|loss\s+function)\b",
]


def sanitize_sources(sources: List[str]) -> List[str]:
    """
    Sanitizes retrieved sources metadata so no internal/model leaks appear.
    If any chunk title contains 'Llama' or 'System Prompt', replaces it with 'Farmer Advisory Guidelines'.
    Also scrubs any forbidden technical jargon patterns from source titles.
    """
    sanitized: List[str] = []
    for s in sources:
        if not s or not isinstance(s, str):
            continue
        # If chunk title contains "Llama" or "System Prompt", replace with "Farmer Advisory Guidelines"
        if re.search(r"\b(llama|system\s*prompt)\b", s, flags=re.IGNORECASE):
            clean_s = "Farmer Advisory Guidelines"
        else:
            clean_s = s
            clean_s = clean_s.replace("**", "").replace("*", "")
            for pattern in LEAKAGE_BLACKLIST_PATTERNS:
                clean_s = re.sub(pattern, "", clean_s, flags=re.IGNORECASE)
            clean_s = clean_s.strip()
            if not clean_s:
                clean_s = "Farmer Advisory Guidelines"
        if clean_s not in sanitized:
            sanitized.append(clean_s)
    return sanitized if sanitized else ["ICAR Advisory Directory"]


class RAGPipeline:
    """
    Offline RAG Advisory Pipeline interfacing with ChromaStore and local Ollama.
    Guarantees zero technical leakage and provides robust offline fallback.
    """

    def __init__(
        self,
        ollama_url: str = "http://127.0.0.1:11434",
        model_name: str = "llama3.2:1b",
        chroma_store: Optional[ChromaStore] = None
    ):
        self.ollama_url = ollama_url.rstrip("/")
        self.model_name = model_name
        self.store = chroma_store or get_chroma_store()
        self.http_client = httpx.Client(base_url=self.ollama_url, timeout=30.0)

    def _determine_urgency(self, query: str, context: str) -> str:
        urgent_keywords = [
            "severe", "blight", "hopper burn", "armyworm", "cyclone", "flood",
            "rot", "frost", "urgent", "dying", "outbreak", "infestation", "wilting"
        ]
        text = (query + " " + context).lower()
        if any(kw in text for kw in urgent_keywords):
            return "Urgent"

        advisory_keywords = [
            "dose", "fertilizer", "spray", "subsidy", "ph", "irrigation",
            "spacing", "seed rate", "variety", "transplanting", "urea", "dap", "mop"
        ]
        if any(kw in text for kw in advisory_keywords):
            return "Advisory"

        return "Normal"

    def scrub_technical_leakage(self, text: str) -> str:
        """Strips or replaces any blacklisted internal technical keywords from generated text."""
        result = text
        for pattern in LEAKAGE_BLACKLIST_PATTERNS:
            result = re.sub(pattern, "", result, flags=re.IGNORECASE)

        # Remove academic ETL jargon
        result = re.sub(r"\bEconomic Threshold Level\s*(?:\(ETL\))?:?\s*", "", result, flags=re.IGNORECASE)
        result = re.sub(r"\bETL:?\s*", "", result, flags=re.IGNORECASE)

        # Post-scrub cleanup for orphan punctuation and connector words left by removals:
        for _ in range(3):
            # Dangling determiners/pronouns stranded before punctuation
            result = re.sub(r"\b(a|an|the|its|their|this|that|these|those|my|your|our)\s*([,\.!?])", r"\2", result, flags=re.IGNORECASE)
            # Dangling prepositions or conjunctions stranded before punctuation (e.g. "powered by and.", "3.2B and.")
            result = re.sub(r"\b(and|or|by|at|in|on|with|to|for|about|of)\s*([,\.!?])", r"\2", result, flags=re.IGNORECASE)
            # Dangling conjunctions before punctuation: e.g. ", or ." -> "."
            result = re.sub(r",\s*(?:and|or|but)?\s*([,\.!?])", r"\1", result, flags=re.IGNORECASE)
            # Clean orphan spaces before punctuation: " ." -> "." or " ," -> ","
            result = re.sub(r"\s+([,\.!?])", r"\1", result)
            # Clean repeated punctuation: ", ," -> "," or ",." -> "." or ".." -> "."
            result = re.sub(r",\s*,+", ",", result)
            result = re.sub(r",\s*\.", ".", result)
            result = re.sub(r"\.{2,}", ".", result)

        # Clean empty parentheses left behind by scrubbed parameters: e.g. "()", "(, )", "( , )"
        result = re.sub(r"\(\s*[,;\s]*\)", "", result)

        # Normalize multiple spaces and blank lines
        result = re.sub(r"[ \t]+", " ", result)
        result = re.sub(r"\n\s*\n\s*\n+", "\n\n", result)
        # Clean trailing connectors left stranded at the end of text
        result = re.sub(r"\b(and|or|by|at|in|on|with|to|for|about|of)\s*$", "", result.strip(), flags=re.IGNORECASE)
        return result.strip()

    def _build_fallback_advisory(
        self,
        query: str,
        retrieved_docs: List[Dict[str, Any]],
        crop_name: Optional[str],
        language: str = "en"
    ) -> str:
        """
        Synthesize clean, structured agronomic advice directly from retrieved
        ICAR/TNAU chunks in the farmer's native language.
        """
        points = []
        if retrieved_docs:
            for d in retrieved_docs[:3]:
                txt = d["text"].strip()
                lines = [l.strip() for l in txt.split("\n") if l.strip()]
                for l in lines:
                    # Filter out academic ETL / threshold lines
                    if any(bad in l.lower() for bad in ["etl", "economic threshold", "threshold level"]):
                        continue
                    if any(k in l.lower() for k in ["spray", "apply", "dose", "rate", "control", "action", "spacing", "fertilizer"]):
                        clean_l = l.replace("**", "").replace("*", "")
                        if clean_l not in points:
                            points.append(clean_l)
                            if len(points) >= 4:
                                break
                if len(points) >= 4:
                    break

            if not points:
                for d in retrieved_docs[:2]:
                    first_lines = d["text"].strip().split("\n")[:2]
                    for l in first_lines:
                        clean_l = l.replace("**", "").replace("*", "")
                        if any(bad in clean_l.lower() for bad in ["etl", "economic threshold", "threshold level"]):
                            continue
                        if clean_l and clean_l not in points:
                            points.append(clean_l)

        # Route all queries (including English) through structured, jargon-free farmer advisory engine
        return localize_fallback_advisory(language or "en", crop_name, points, query=query)

    def ask(
        self,
        query: str,
        crop_name: Optional[str] = None,
        vision_context: Optional[str] = None,
        n_chunks: int = 4,
        language: str = "en"
    ) -> AdvisoryResult:
        """
        Generate grounded agronomic advisory for a farmer query in their native language.
        """
        search_query = f"{crop_name} {query}" if crop_name else query
        retrieved = self.store.query(search_query, n_results=n_chunks)

        context_blocks = "\n---\n".join([r["text"] for r in retrieved])
        raw_sources = list(dict.fromkeys([r["metadata"].get("topic", r["metadata"].get("section", "ICAR Package of Practices")) for r in retrieved])) or ["ICAR Guidelines"]
        sources = sanitize_sources(raw_sources)
        urgency = self._determine_urgency(query, context_blocks)

        lang_code = language.lower() if language else "en"
        lang_directive = get_language_directive(lang_code)
        system_prompt = f"{FARMER_SYSTEM_PROMPT}\n\n{lang_directive}"

        prompt_vision = f"Vision Health Findings: {vision_context}" if vision_context else ""
        prompt_content = FARMER_PROMPT_TEMPLATE.format(
            retrieved_context=context_blocks if context_blocks else "General agricultural guidelines apply.",
            query=query,
            vision_context=prompt_vision
        )
        if lang_code != "en":
            prompt_content += f"\n\n{lang_directive}"

        # 1. Attempt ExecuTorch reference runtime on Arm CPU if available
        executorch_url = os.environ.get("EXECUTORCH_URL", "http://127.0.0.1:8008/generate")
        try:
            et_resp = httpx.post(
                executorch_url,
                json={"prompt": prompt_content, "system_prompt": system_prompt, "language": lang_code},
                timeout=30.0
            )
            if et_resp.status_code == 200:
                raw_answer = et_resp.json().get("response", "")
                if raw_answer:
                    clean_answer = self.scrub_technical_leakage(raw_answer)
                    if "1800-180-1551" not in clean_answer:
                        clean_answer += "\n\nFor immediate free telephonic guidance, contact the toll-free Kisan Call Centre helpline at 1800-180-1551 (6:00 AM to 10:00 PM)."
                    return AdvisoryResult(
                        query=query,
                        crop_name=crop_name,
                        answer=clean_answer,
                        sources=sources,
                        urgency_level=urgency
                    )
        except Exception:
            pass

        # 2. Attempt Ollama LLaMA service (Host GPU / CPU)
        try:
            resp = self.http_client.post(
                "/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt_content}
                    ],
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 450}
                }
            )
            if resp.status_code == 200:
                raw_answer = resp.json().get("message", {}).get("content", "")
                clean_answer = self.scrub_technical_leakage(raw_answer)

                if "1800-180-1551" not in clean_answer:
                    clean_answer += "\n\nFor immediate free telephonic guidance, contact the toll-free Kisan Call Centre helpline at 1800-180-1551 (6:00 AM to 10:00 PM)."

                return AdvisoryResult(
                    query=query,
                    crop_name=crop_name,
                    answer=clean_answer,
                    sources=sources,
                    urgency_level=urgency
                )
        except Exception:
            pass

        # Robust offline fallback path
        fallback_answer = self._build_fallback_advisory(query, retrieved, crop_name, language=lang_code)
        return AdvisoryResult(
            query=query,
            crop_name=crop_name,
            answer=fallback_answer,
            sources=sources,
            urgency_level=urgency
        )

    def generate_advisory(
        self,
        query: str,
        crop_name: Optional[str] = None,
        vision_context: Optional[str] = None,
        n_chunks: int = 4,
        language: str = "en"
    ) -> AdvisoryResult:
        """Alias for ask() for API backwards compatibility."""
        return self.ask(query=query, crop_name=crop_name, vision_context=vision_context, n_chunks=n_chunks, language=language)

    def ask_stream(
        self,
        query: str,
        crop_name: Optional[str] = None,
        vision_context: Optional[str] = None,
        n_chunks: int = 4
    ) -> Generator[str, None, None]:
        """
        Stream grounded tokens for real-time responsiveness over the local Wi-Fi hotspot.
        """
        search_query = f"{crop_name} {query}" if crop_name else query
        retrieved = self.store.query(search_query, n_results=n_chunks)
        context_blocks = "\n---\n".join([r["text"] for r in retrieved])

        prompt_vision = f"Vision Health Findings: {vision_context}" if vision_context else ""
        prompt_content = FARMER_PROMPT_TEMPLATE.format(
            retrieved_context=context_blocks if context_blocks else "General agricultural guidelines apply.",
            query=query,
            vision_context=prompt_vision
        )

        try:
            with self.http_client.stream(
                "POST",
                "/api/chat",
                json={
                    "model": self.model_name,
                    "messages": [
                        {"role": "system", "content": FARMER_SYSTEM_PROMPT},
                        {"role": "user", "content": prompt_content}
                    ],
                    "stream": True,
                    "options": {"temperature": 0.2, "num_predict": 450}
                }
            ) as response:
                if response.status_code == 200:
                    for line in response.iter_lines():
                        if line:
                            chunk = json.loads(line)
                            token = chunk.get("message", {}).get("content", "")
                            if token:
                                # Quick sanitize token
                                clean_token = self.scrub_technical_leakage(token)
                                yield clean_token
                            if chunk.get("done", False):
                                break
                    return
        except Exception:
            pass

        # Fallback stream
        fallback = self._build_fallback_advisory(query, retrieved, crop_name)
        yield fallback

    def stream_advisory(
        self,
        query: str,
        crop_name: Optional[str] = None,
        vision_context: Optional[str] = None,
        n_chunks: int = 4
    ) -> Generator[str, None, None]:
        """Alias for ask_stream() for API backwards compatibility."""
        return self.ask_stream(query=query, crop_name=crop_name, vision_context=vision_context, n_chunks=n_chunks)


# Alias class name for flexible imports
RagPipeline = RAGPipeline
