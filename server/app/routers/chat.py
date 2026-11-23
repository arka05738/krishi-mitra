"""
Chat API Router for Multi-Turn Farmer Conversational Interaction.
Maintains conversational grounding via ICAR ChromaDB vector retrieval and local Ollama LLM.
Supports /api/chat/message.
"""
import re
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException

from server.app.rag.rag_pipeline import (
    RAGPipeline,
    FARMER_SYSTEM_PROMPT,
    FARMER_PROMPT_TEMPLATE,
    sanitize_sources,
)
from server.app.rag.multilingual import (
    get_language_directive,
    INDIC_LANGUAGES,
    localize_fallback_advisory,
    localize_sources,
    get_localized_emergency_contact,
    _match_topic_key,
)
from server.app.rag.chroma_store import get_chroma_store
from server.app.schemas.api_models import ChatRequest, ChatResponse, LocalizeChatRequest
from server.app.routers.advisory import get_rag, PROBING_KEYWORDS

EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001FAFF\U0001F1E6-\U0001F1FF\U00002600-\U000027BF\u200D\uFE0E\uFE0F]"
)

router = APIRouter(prefix="/api/chat", tags=["Chat"])

CROPS = ["potato", "tomato", "rice", "wheat", "sunflower", "maize", "corn", "mustard", "cotton", "soybean", "chilli"]


@router.post("/message", response_model=ChatResponse)
async def chat_message(payload: Dict[str, Any]) -> ChatResponse:
    """Multi-turn farmer chat endpoint with zero-jargon ICAR grounding."""
    raw_msg = payload.get("message") or payload.get("question")
    if not raw_msg or not str(raw_msg).strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    clean_msg = EMOJI_PATTERN.sub("", str(raw_msg))
    clean_msg = re.sub(r"[\x00-\x1f\x7f-\x9f\u200b-\u200f\ufeff]", "", clean_msg).strip()
    if not clean_msg or not any(c.isprintable() and not c.isspace() for c in clean_msg):
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    msg_lower = clean_msg.lower()

    # 1. Adversarial Model Name / Architecture Extraction Defense (Zero Tech Leakage)
    if any(kw in msg_lower for kw in PROBING_KEYWORDS):
        greeting = (
            "I am Krishi Mitra, an agricultural advisory assistant trained on Indian agricultural guidelines from ICAR "
            "and State Agricultural Universities to assist farmers with crop health, pest remedies, and fertilizer guidance.\n\n"
            "For immediate free telephonic guidance, contact the toll-free Kisan Call Centre helpline at 1800-180-1551 (6:00 AM to 10:00 PM)."
        )
        return ChatResponse(
            reply=greeting,
            response=greeting,
            sources=["ICAR Kharif Agro-Advisories", "TNAU Agritech Portal"],
            urgency_level="Normal",
            helpline="Kisan Call Centre: 1800-180-1551"
        )

    history = payload.get("history", [])
    hist_text = " ".join([
        h.get("content", "") for h in history if isinstance(h, dict) and h.get("content")
    ])
    combined_query = f"Context: {hist_text}. Question: {clean_msg}" if hist_text else clean_msg

    # 2. Detect crop context from current message or conversation history
    crop_hint = payload.get("crop_name")
    if not crop_hint:
        combined_lower = (clean_msg + " " + hist_text).lower()
        for crop in CROPS:
            if crop in combined_lower:
                crop_hint = crop.capitalize()
                break

    rag = get_rag()
    store = get_chroma_store()

    # 3. Retrieve authoritative ICAR chunks
    search_query = f"{crop_hint} {clean_msg}" if crop_hint else clean_msg
    retrieved = await asyncio.to_thread(store.query, search_query, 4)
    context_blocks = "\n---\n".join([r["text"] for r in retrieved]) if retrieved else ""
    raw_sources = list(dict.fromkeys([
        r["metadata"].get("topic", r["metadata"].get("section", "ICAR Advisory Directory"))
        for r in retrieved
    ])) or ["ICAR Advisory Directory"]
    sources = sanitize_sources(raw_sources)

    urgency = rag._determine_urgency(clean_msg, context_blocks)
    lang = str(payload.get("language") or "en").lower()
    lang_directive = get_language_directive(lang)

    # 4. Attempt multi-turn Ollama generation
    try:
        sys_msg = f"{FARMER_SYSTEM_PROMPT}\n\n{lang_directive}"
        messages = [{"role": "system", "content": sys_msg}]
        if history:
            for turn in history[-6:]:
                if isinstance(turn, dict):
                    role = turn.get("role", "user")
                    content = turn.get("content", "")
                    if role in ("user", "assistant") and content:
                        messages.append({"role": role, "content": content})

        prompt_content = FARMER_PROMPT_TEMPLATE.format(
            retrieved_context=context_blocks if context_blocks else "General agricultural guidelines apply.",
            query=clean_msg,
            vision_context=""
        )
        if lang != "en":
            prompt_content += f"\n\n{lang_directive}"
        messages.append({"role": "user", "content": prompt_content})

        def call_ollama():
            return rag.http_client.post(
                "/api/chat",
                json={
                    "model": rag.model_name,
                    "messages": messages,
                    "stream": False,
                    "options": {"temperature": 0.2, "num_predict": 450}
                }
            )

        resp = await asyncio.to_thread(call_ollama)
        if resp.status_code == 200:
            raw_reply = resp.json().get("message", {}).get("content", "")
            clean_reply = rag.scrub_technical_leakage(raw_reply)
            clean_reply = EMOJI_PATTERN.sub("", clean_reply).strip()
            if "1800-180-1551" not in clean_reply:
                clean_reply += "\n\nFor immediate free telephonic guidance, contact the toll-free Kisan Call Centre helpline at 1800-180-1551 (6:00 AM to 10:00 PM)."

            return ChatResponse(
                reply=clean_reply,
                response=clean_reply,
                sources=sources,
                urgency_level=urgency,
                helpline="Kisan Call Centre: 1800-180-1551"
            )
    except Exception:
        pass

    # 5. Graceful offline fallback synthesizing retrieved ICAR chunks in native language
    fallback_res = await asyncio.to_thread(
        rag.generate_advisory,
        query=combined_query,
        crop_name=crop_hint,
        language=lang
    )
    clean_fallback = EMOJI_PATTERN.sub("", fallback_res.answer).strip()

    return ChatResponse(
        reply=clean_fallback,
        response=clean_fallback,
        sources=sanitize_sources(fallback_res.sources if fallback_res.sources else sources),
        urgency_level=fallback_res.urgency_level,
        helpline=fallback_res.helpline
    )


CHAT_GREETINGS = {
    "en": "Namaste Kisan Bhai. I am your Krishi Mitra Advisory Assistant. Tap the microphone to speak your question, or type below.",
    "hi": "नमस्ते किसान भाई। मैं आपका कृषि मित्र सलाहकार हूँ। अपनी भाषा में बोलकर या लिखकर फसल रोग, खाद या योजनाओं के बारे में पूछें।",
    "bn": "নমস্কার কৃষক ভাই। আমি আপনার কৃষি মিত্র উপদেষ্টা। মুখে বলে বা লিখে ফসলের রোগ, সার বা সরকারি প্রকল্প সম্পর্কে প্রশ্ন করুন।",
    "te": "నమస్కారం రైతు సోదరా. నేను మీ కృషి మిత్ర సలహాదారుని. మాట్లాడి లేదా టైప్ చేసి మీ వ్యవసాయ ప్రశ్నలను అడగండి.",
    "ta": "வணக்கம் விவசாய தோழரே. நான் உங்கள் கிருஷி மித்ரா ஆலோசகர். குரல் வழியாகவோ அல்லது தட்டச்சு செய்தோ விவசாய கேள்விகளைக் கேளுங்கள்.",
    "mr": "नमस्कार शेतकरी बांधवांनो. मी आपला कृषी मित्र सल्लागार आहे. बोलून किंवा लिहून शेतीविषयक कोणतेही प्रश्न विचारा.",
    "gu": "નમસ્તે ખેડૂત મિત્ર. હું તમારો કૃષિ મિત્ર સલાહકાર છું. બોલીને કે લખીને ખેતીના પ્રશ્નો પૂછો.",
    "kn": "ನಮಸ್ಕಾರ ರೈತ ಬಾಂಧವರೇ. ನಾನು ನಿಮ್ಮ ಕೃಷಿ ಮಿತ್ರ ಸಲಹೆಗಾರ. ಧ್ವನಿಯ ಮೂಲಕ ಅಥವಾ ಬರೆದು ಕೃಷಿ ಪ್ರಶ್ನೆಗಳನ್ನು ಕೇಳಿ.",
    "ml": "നമസ്കാരം കർഷക സുഹൃത്തേ. ഞാൻ നിങ്ങളുടെ കൃഷി മിത്ര ഉപദേശകനാണ്. സംസാരിച്ചോ എഴുതിയോ കൃഷി ചോദ്യങ്ങൾ ചോദിക്കാം.",
    "pa": "ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ ਕਿਸਾਨ ਵੀਰੋ। ਮੈਂ ਤੁਹਾਡਾ ਕ੍ਰਿਸ਼ੀ ਮਿੱਤਰ ਸਲਾਹਕਾਰ ਹਾਂ। ਬੋਲ ਕੇ ਜਾਂ ਲਿਖ ਕੇ ਖੇਤੀਬਾੜੀ ਬਾਰੇ ਕੋਈ ਵੀ ਸਵਾਲ ਪੁੱਛੋ।",
    "or": "ନମସ୍କାର ଚାଷୀ ଭାଇ। ମୁଁ ଆପଣଙ୍କ କୃଷି ମିତ୍ର ପରାମର୍ଶଦାତା। କହି କିମ୍ବା ଲେଖି ଚାଷ ସମ୍ପର୍କିତ ପ୍ରଶ୍ନ ପଚାରନ୍ତୁ।",
    "as": "নমস্কাৰ কৃষক ভাই। মই আপোনাৰ কৃষি মিত্ৰ সহায়ক। কথা কৈ বা লিখি খেতিৰ বিষয়ে সুধিব পাৰে।",
    "ur": "آداب کسان بھائی۔ میں آپ کا زرعی مشیر ہوں۔ بول کر یا لکھ کر زراعت اور فصلوں کے بارے में सवाल پوچھیں۔",
}


@router.post("/re-localize")
async def re_localize_chat_messages(payload: LocalizeChatRequest):
    """Dynamically re-localizes an entire chat conversation into the newly selected language."""
    target_lang = (payload.language or "en").lower()
    updated_messages = []

    for idx, msg in enumerate(payload.messages):
        role = msg.get("role", "user")
        content = msg.get("content", "")
        updated_msg = dict(msg)

        if role == "assistant":
            # If initial welcome greeting
            if idx == 0 or "Krishi Mitra" in content or "কৃষি মিত্র" in content or "कृषि मित्र" in content:
                updated_msg["content"] = CHAT_GREETINGS.get(target_lang, CHAT_GREETINGS["en"])
                updated_msg["sources"] = localize_sources(["ICAR Package of Practices"], target_lang)
                updated_msg["helpline"] = get_localized_emergency_contact(target_lang)
            else:
                # Advisory answer re-localization
                topic = _match_topic_key(content)
                updated_msg["content"] = localize_fallback_advisory(target_lang, None, [], query=content)
                updated_msg["sources"] = localize_sources(msg.get("sources", ["ICAR Package of Practices"]), target_lang)
                updated_msg["helpline"] = get_localized_emergency_contact(target_lang)
        elif role == "user":
            # If standard consultation prompt: "How to treat X in Y?"
            lower_c = content.lower()
            if "late blight" in lower_c or "নাবী ধসা" in lower_c or "पछेती झुलसा" in lower_c:
                if target_lang == "bn":
                    updated_msg["content"] = "টমেটো বা আলুতে নাবী ধসা রোগ কীভাবে চিকিৎসা করবেন?"
                elif target_lang == "hi":
                    updated_msg["content"] = "टमाटर या आलू में पछेती झुलसा रोग का उपचार कैसे करें?"
                else:
                    updated_msg["content"] = "How to treat Late Blight in Tomato or Potato?"
            elif "early blight" in lower_c or "আগাম ধসা" in lower_c or "अगेती झुलसा" in lower_c:
                if target_lang == "bn":
                    updated_msg["content"] = "টমেটোতে আগাম ধসা রোগ কীভাবে নিরাময় করবেন?"
                elif target_lang == "hi":
                    updated_msg["content"] = "टमाटर में अगेती झुलसा का उपचार कैसे करें?"
                else:
                    updated_msg["content"] = "How to treat Early Blight in Tomato?"

        updated_messages.append(updated_msg)

    return {"messages": updated_messages}
