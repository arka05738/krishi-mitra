"""
Automated Unit and Integration Test Suite for Milestone M2: offline_rag_advisory_engine.
Verifies table-row-aware semantic chunking (all chunks <= 256 tokens),
offline ChromaDB store persistence and vector retrieval,
12-parameter Soil Health Card diagnostic & commercial fertilizer engine,
and farmer-facing RAG advisory pipeline with zero-tech-leakage enforcement.
"""

import os
import re
import pytest
from pathlib import Path

# Enforce strict offline execution
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

from server.app.rag.knowledge_ingestion import (
    KnowledgeBaseChunker,
    parse_knowledge_base,
    ingest_knowledge_base,
    clean_agronomic_text,
)
from server.app.rag.chroma_store import (
    LocalMiniLMEmbeddingFunction,
    ChromaStore,
    get_chroma_store,
)
from server.app.rag.soil_calculator import (
    SoilReportInput,
    SoilReportOutput,
    calculate_soil_health,
    calculate_fertilizer_recommendation,
    classify_soil_ph,
    classify_ec,
    classify_oc,
    classify_primary_nutrient,
    get_crop_profile,
    CROP_DATABASE,
)
from server.app.rag.rag_pipeline import (
    RAGPipeline,
    AdvisoryResult,
    FARMER_SYSTEM_PROMPT,
)


PROJECT_ROOT = Path(__file__).resolve().parent.parent
KB_PATH = PROJECT_ROOT / "Advisory data" / "india_farmer_advisory_rag_knowledge_base.md"


# ==============================================================================
# TEST SUITE 1: OFFLINE EMBEDDING MODEL & TOKENIZER
# ==============================================================================

def test_offline_embedding_model_loading():
    """Verify sentence-transformers/all-MiniLM-L6-v2 loads locally without internet."""
    from sentence_transformers import SentenceTransformer
    model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", local_files_only=True)
    assert model.max_seq_length == 256
    dim = model.get_embedding_dimension() if hasattr(model, "get_embedding_dimension") else model.get_sentence_embedding_dimension()
    assert dim == 384

    embeddings = model.encode(["Paddy blast disease control", "Neem-coated urea dosage"])
    assert embeddings.shape == (2, 384)


def test_clean_agronomic_text():
    """Verify LaTeX math and markdown link stripping."""
    raw = r"Apply $\text{kg/ha}$ of $\text{P}_2\text{O}_5$ at $12–18^\circ\text{C}$ see [CIP SOP](https://cipotato.org/sop.pdf)"
    cleaned = clean_agronomic_text(raw)
    assert r"\text" not in cleaned
    assert "$" not in cleaned
    assert "https://cipotato.org" not in cleaned
    assert "CIP SOP" in cleaned
    assert "kg/ha" in cleaned
    assert "P2O5" in cleaned


# ==============================================================================
# TEST SUITE 2: TABLE-AWARE KNOWLEDGE BASE CHUNKING (<= 256 TOKENS)
# ==============================================================================

def test_knowledge_base_chunking_token_limits():
    """
    Verify that parse_knowledge_base splits the master knowledge base
    into at least 120 semantic chunks and EVERY chunk is <= 256 tokens.
    """
    assert KB_PATH.exists(), f"Knowledge base file not found at {KB_PATH}"

    chunks = parse_knowledge_base(KB_PATH)
    assert len(chunks) == 122, f"Expected exactly 122 chunks, got {len(chunks)}"

    over_limit_chunks = [c for c in chunks if c.token_count > 256]
    assert len(over_limit_chunks) == 0, (
        f"{len(over_limit_chunks)} chunks exceed 256 tokens! "
        f"Worst offender: {over_limit_chunks[0].chunk_id} with {over_limit_chunks[0].token_count} tokens"
    )

    max_tokens = max(c.token_count for c in chunks)
    min_tokens = min(c.token_count for c in chunks)
    assert max_tokens <= 256
    assert min_tokens >= 50

    # Verify metadata fields
    for c in chunks:
        assert c.chunk_id
        assert c.metadata["section"]
        assert c.metadata["crop"]
        assert c.metadata["topic"]
        assert c.metadata["source"]
        assert c.metadata["helpline"] == "1800-180-1551"
        assert c.metadata["doc_type"] in ("table", "narrative")


# ==============================================================================
# TEST SUITE 3: CHROMADB STORE PERSISTENCE & VECTOR RETRIEVAL
# ==============================================================================

def test_chroma_store_temporary_instance(tmp_path):
    """Verify ChromaStore document addition, count, and vector search on isolated dir."""
    test_dir = str(tmp_path / "test_chroma")
    store = ChromaStore(persist_dir=test_dir)
    assert store.count() == 0
    assert not store.is_indexed()

    store.add_documents(
        documents=[
            "Tomato early blight can be managed by spraying Mancozeb 75 WP at 2.0 to 2.5 g/L.",
            "Wheat requires critical irrigation at CRI stage (20 to 25 days after sowing)."
        ],
        metadatas=[{"crop": "Tomato", "topic": "Early Blight"}, {"crop": "Wheat", "topic": "Irrigation"}],
        ids=["doc_tomato", "doc_wheat"]
    )
    assert store.count() == 2
    assert store.is_indexed()

    results = store.query("How to manage tomato blight?", n_results=1)
    assert len(results) == 1
    assert "Mancozeb" in results[0]["text"]
    assert results[0]["metadata"]["crop"] == "Tomato"
    assert results[0]["distance"] < 0.6


def test_chroma_store_persistent_indexing():
    """Verify that the primary persistent ChromaDB index is populated with master KB chunks."""
    store = get_chroma_store()
    if not store.is_indexed() or store.count() < 122:
        ingest_knowledge_base(force_reindex=True)

    assert store.count() >= 122

    # Query 1: Tomato blight
    res_tomato = store.query("Tomato early blight leaf spots spray", n_results=2)
    assert len(res_tomato) > 0
    assert any("Tomato" in r["text"] or "Blight" in r["text"] for r in res_tomato)

    # Query 2: Soil acidity lime
    res_soil = store.query("Soil pH is 5.2 acidic, what lime should I apply?", n_results=2)
    assert len(res_soil) > 0
    assert any("Lime" in r["text"] or "pH" in r["text"] for r in res_soil)

    # Query 3: PMFBY 72 hours claim
    res_scheme = store.query("Crop destroyed by hailstorm, PMFBY claim intimation window", n_results=2)
    assert len(res_scheme) > 0
    assert any("72" in r["text"] or "PMFBY" in r["text"] for r in res_scheme)


# ==============================================================================
# TEST SUITE 4: SOIL HEALTH CARD 12-PARAMETER CALCULATOR
# ==============================================================================

def test_soil_ph_classification():
    """Test pH classifications and amendment recommendations."""
    # Strongly Acidic
    st, text, lime, gyp = classify_soil_ph(5.2, 1.0)
    assert "Strongly Acidic" in st
    assert lime == 400.0
    assert gyp is None
    assert "Lime" in text

    # Moderately Acidic
    st, text, lime, gyp = classify_soil_ph(6.0, 1.0)
    assert "Moderately Acidic" in st
    assert lime == 300.0
    assert gyp is None

    # Neutral
    st, text, lime, gyp = classify_soil_ph(7.0, 1.0)
    assert "Neutral" in st
    assert text is None
    assert lime is None
    assert gyp is None

    # Moderately Alkaline
    st, text, lime, gyp = classify_soil_ph(8.2, 1.0)
    assert "Moderately Alkaline" in st
    assert gyp == 400.0
    assert lime is None

    # Sodic / Alkali
    st, text, lime, gyp = classify_soil_ph(8.8, 1.0)
    assert "Sodic" in st
    assert gyp == 600.0
    assert lime is None


def test_soil_ec_and_oc_classification():
    """Test EC salinity and OC soil health classification."""
    assert "Normal" in classify_ec(0.6)
    assert "Critical" in classify_ec(1.4)
    assert "Saline" in classify_ec(3.2)

    assert "Low" in classify_oc(0.35)
    assert "Medium" in classify_oc(0.60)
    assert "High" in classify_oc(0.85)


def test_stcr_nutrient_adjustment_factors():
    """Test Low (+25%), Medium (0%), High (-25%) STCR adjustments."""
    cat, factor = classify_primary_nutrient(200.0, "n")
    assert "Low" in cat and factor == 1.25

    cat, factor = classify_primary_nutrient(350.0, "n")
    assert "Medium" in cat and factor == 1.00

    cat, factor = classify_primary_nutrient(600.0, "n")
    assert "High" in cat and factor == 0.75

    cat, factor = classify_primary_nutrient(15.0, "p2o5")
    assert "Low" in cat and factor == 1.25

    cat, factor = classify_primary_nutrient(70.0, "p2o5")
    assert "High" in cat and factor == 0.75

    cat, factor = classify_primary_nutrient(100.0, "k2o")
    assert "Low" in cat and factor == 1.25

    cat, factor = classify_primary_nutrient(300.0, "k2o")
    assert "High" in cat and factor == 0.75


def test_worked_example_pair_1_rice():
    """
    Test Worked Example 1: Kharif Aman Rice for 1 Hectare (2.47105 acres).
    Grounded in CHUNK-16 Gold Benchmark Pair 1.
    """
    inp = SoilReportInput(
        crop="rice",
        area_acres=2.47105,  # Exactly 1.0 ha
        nitrogen=210.0,      # Low (< 280) -> +25% (100 kg N/ha)
        phosphorus=35.0,     # Medium (23–57) -> 100% (40 kg P2O5/ha)
        potassium=190.0,     # Medium (120–280) -> 100% (40 kg K2O/ha)
        ph=5.8,              # Moderately Acidic -> Lime 300 kg/ha
        electrical_conductivity=0.6,
        organic_carbon=0.45
    )
    out = calculate_soil_health(inp)

    assert "Acidic" in out.ph_status
    assert out.lime_kg == 300.0
    assert out.dap_kg == 87.0
    # Mandatory DAP-N deduction check:
    # 87 kg DAP supplies 15.65 kg N.
    # Remaining N = 100 - 15.65 = 84.35 kg N.
    # Urea = 84.35 / 0.46 = 183.4 kg.
    assert out.urea_kg == 183.4
    assert out.mop_kg == 66.7
    assert out.zinc_sulphate_kg == 25.0
    assert len(out.application_schedule) >= 3


def test_worked_example_2_wheat_sodic_soil():
    """
    Test Worked Example 2: Timely Sown Irrigated Wheat for 1.0 Acre with Sodic Soil.
    """
    inp = SoilReportInput(
        crop="wheat",
        area_acres=1.0,
        nitrogen=180.0,      # Low -> +25% (150 kg N/ha)
        phosphorus=65.0,     # High -> -25% (45 kg P2O5/ha)
        potassium=210.0,     # Medium -> 0% (40 kg K2O/ha)
        ph=8.6,              # Sodic -> Gypsum @ 600 kg/ha -> 242.8 kg/acre
        electrical_conductivity=1.4,
        organic_carbon=0.38,
        zinc=0.4             # Deficient Zn -> ZnSO4 @ 25 kg/ha -> 10.1 kg/acre
    )
    out = calculate_soil_health(inp)

    assert "Sodic" in out.ph_status
    assert out.gypsum_kg == 242.8
    assert out.dap_kg == 39.6
    assert out.urea_kg == 116.5
    assert out.mop_kg == 27.0
    assert out.zinc_sulphate_kg == 10.1


def test_worked_example_3_tomato_neutral_soil():
    """
    Test Worked Example 3: F1 Hybrid Tomato for 0.5 Acre with Optimal Soil.
    """
    inp = SoilReportInput(
        crop="tomato",
        area_acres=0.5,
        nitrogen=320.0,      # Medium -> 150 kg N/ha
        phosphorus=45.0,     # Medium -> 75 kg P2O5/ha
        potassium=220.0,     # Medium -> 75 kg K2O/ha
        ph=6.8,              # Neutral -> None
        electrical_conductivity=0.5,
        organic_carbon=0.65
    )
    out = calculate_soil_health(inp)

    assert "Neutral" in out.ph_status
    assert out.amendment_needed is None
    assert out.dap_kg == 33.0
    assert out.urea_kg == 53.1
    assert out.mop_kg == 25.3


def test_dap_n_excess_clamping():
    """
    Edge case: when DAP supplies more N than total required N (e.g. legume starter),
    Urea must safely clamp to 0.0 kg and never be negative.
    """
    inp = SoilReportInput(
        crop="chickpea",     # Base: 20 N : 40 P : 20 K
        area_acres=1.0,
        nitrogen=600.0,      # High N -> -25% -> 15 kg N/ha
        phosphorus=20.0,     # Low P -> +25% -> 50 kg P2O5/ha
        potassium=200.0,
        ph=7.0,
        electrical_conductivity=0.5,
        organic_carbon=0.6
    )
    out = calculate_soil_health(inp)
    assert out.urea_kg == 0.0
    assert out.dap_kg > 0.0


def test_crop_synonyms_and_aliases():
    """Verify crop name aliases map to the intended crop database profiles."""
    assert get_crop_profile("Paddy")["display_name"].startswith("Rice")
    assert get_crop_profile("Aman Dhan")["display_name"].startswith("Rice")
    assert get_crop_profile("Swarna")["display_name"].startswith("Rice")
    assert get_crop_profile("Corn")["display_name"].startswith("Maize")
    assert get_crop_profile("Sarson")["display_name"].startswith("Rapeseed")
    assert get_crop_profile("Aloo")["display_name"].startswith("Potato")
    assert get_crop_profile("Baingan")["display_name"].startswith("Brinjal")


def test_soil_calculator_empty_crop_fallback():
    """Verify that crop='' or crop='   ' safely falls back to default field crop RDF (100:50:50)."""
    default_profile = CROP_DATABASE["default"]
    assert get_crop_profile("") == default_profile
    assert get_crop_profile("   ") == default_profile
    assert get_crop_profile(crop_name="") == default_profile
    assert get_crop_profile(crop_name="   ") == default_profile

    assert default_profile["base_rdf"]["n"] == 100.0
    assert default_profile["base_rdf"]["p2o5"] == 50.0
    assert default_profile["base_rdf"]["k2o"] == 50.0

    inp_empty = SoilReportInput(
        crop="",
        area_acres=1.0,
        nitrogen=300.0,
        phosphorus=30.0,
        potassium=150.0,
        ph=7.0,
        electrical_conductivity=0.5,
        organic_carbon=0.6
    )
    out_empty = calculate_soil_health(inp_empty)
    assert out_empty is not None
    assert out_empty.dap_kg > 0
    assert out_empty.urea_kg > 0
    assert out_empty.mop_kg > 0

    inp_whitespace = SoilReportInput(
        crop="   ",
        area_acres=1.0,
        nitrogen=300.0,
        phosphorus=30.0,
        potassium=150.0,
        ph=7.0,
        electrical_conductivity=0.5,
        organic_carbon=0.6
    )
    out_ws = calculate_soil_health(inp_whitespace)
    assert out_ws.urea_kg == out_empty.urea_kg
    assert out_ws.dap_kg == out_empty.dap_kg
    assert out_ws.mop_kg == out_empty.mop_kg


# ==============================================================================
# TEST SUITE 5: RAG ADVISORY PIPELINE & ZERO TECH LEAKAGE
# ==============================================================================

def test_scrubber_filters_models_and_parameters():
    """Verify that model, models, parameter, parameters, llama3.2, chroma are scrubbed cleanly without dangling .2 or broken punctuation."""
    pipeline = RAGPipeline()

    test_str1 = "I can't provide a response that includes technical details about a model, its parameters, or system prompt."
    scrubbed1 = pipeline.scrub_technical_leakage(test_str1)

    for term in ["model", "models", "parameter", "parameters", "system prompt", "prompt"]:
        assert re.search(rf"\b{term}\b", scrubbed1, re.IGNORECASE) is None, f"Term '{term}' found in: {scrubbed1}"
    assert ", or ." not in scrubbed1
    assert " , " not in scrubbed1
    assert scrubbed1.endswith(".")

    test_str2 = "This model uses 7B parameters and llama3.2 with chroma."
    scrubbed2 = pipeline.scrub_technical_leakage(test_str2)
    for term in ["model", "models", "parameter", "parameters", "llama3.2", "llama3", "llama", "chroma"]:
        assert re.search(rf"\b{term}\b", scrubbed2, re.IGNORECASE) is None, f"Term '{term}' found in: {scrubbed2}"
    assert ".2" not in scrubbed2
    assert "  " not in scrubbed2

    test_str3 = "I am an AI assistant powered by llama3.2 and chromadb."
    scrubbed3 = pipeline.scrub_technical_leakage(test_str3)
    for term in ["ai", "llama3.2", "llama3", "llama", "chromadb", "chroma"]:
        assert re.search(rf"\b{term}\b", scrubbed3, re.IGNORECASE) is None, f"Term '{term}' found in: {scrubbed3}"
    assert ".2" not in scrubbed3

def test_rag_pipeline_zero_tech_leakage_and_helpline():
    """Verify RAG advisory generation produces zero technical words and includes helpline."""
    pipeline = RAGPipeline()
    result = pipeline.ask(
        query="My potato field has water-soaked brown lesions on leaves and white cottony growth underneath. What should I spray?",
        crop_name="Potato"
    )

    assert isinstance(result, AdvisoryResult)
    assert len(result.answer) > 50
    assert "1800-180-1551" in result.answer
    assert "1800-180-1551" in result.helpline
    assert result.urgency_level in ("Normal", "Advisory", "Urgent")
    assert len(result.sources) > 0

    # Strict check for forbidden jargon
    blacklisted = [
        r"\bAI\b", r"\bLLM\b", r"\bllama\b", r"\bllama3\b",
        r"\bchromadb?\b", r"\bvector\b", r"\bembeddings?\b",
        r"\bprompt\b", r"\btokens?\b"
    ]
    for pattern in blacklisted:
        match = re.search(pattern, result.answer, re.IGNORECASE)
        assert match is None, f"Found leaked technical term matching '{pattern}' in answer: {result.answer}"


def test_rag_pipeline_offline_fallback():
    """Verify graceful fallback when Ollama is unreachable, returning grounded advice with helpline."""
    # Point to invalid port to simulate offline Ollama failure
    pipeline = RAGPipeline(ollama_url="http://127.0.0.1:59999")
    result = pipeline.ask(
        query="What is the recommended fertilizer schedule and seed rate for timely sown wheat?",
        crop_name="Wheat"
    )

    assert isinstance(result, AdvisoryResult)
    assert len(result.answer) > 80
    assert "1800-180-1551" in result.answer
    assert "Namaste Kisan Bhai" in result.answer
    # No raw connection error stack traces
    assert "ConnectError" not in result.answer
    assert "Traceback" not in result.answer


def test_rag_pipeline_streaming():
    """Verify streaming token generation."""
    pipeline = RAGPipeline()
    tokens = list(pipeline.ask_stream("How to control rice yellow stem borer?", crop_name="Rice"))
    assert len(tokens) > 0
    full_text = "".join(tokens)
    assert len(full_text) > 50
