"""
Unit and integration tests for Multilingual RAG and Voice Assistant.
Tests coverage across all 22 scheduled Indian languages and speech formatting.
"""
import pytest
from fastapi.testclient import TestClient
from server.app.main import app
from server.app.rag.multilingual import (
    SUPPORTED_LANGUAGES,
    SCHEDULED_INDIAN_LANGUAGES,
    get_language_info,
    build_multilingual_prompt_directive,
    clean_markdown_for_speech,
    get_localized_emergency_contact,
)

client = TestClient(app)


def test_22_scheduled_indian_languages_present():
    """Verify that all 22 Eighth Schedule Indian languages are cataloged."""
    assert len(SCHEDULED_INDIAN_LANGUAGES) == 22
    expected_codes = {
        "as", "bn", "brx", "doi", "gu", "hi", "kn", "ks", "kok", "mai",
        "ml", "mni", "mr", "ne", "or", "pa", "sa", "sat", "sd", "ta",
        "te", "ur"
    }
    assert set(SCHEDULED_INDIAN_LANGUAGES.keys()) == expected_codes


def test_supported_languages_includes_english_and_22_local():
    """Verify that SUPPORTED_LANGUAGES includes English + 22 Indian languages = 23 total."""
    assert len(SUPPORTED_LANGUAGES) == 23
    assert "en" in SUPPORTED_LANGUAGES


@pytest.mark.parametrize("code", ["hi", "bn", "te", "ta", "mr", "gu", "kn", "pa"])
def test_language_info_fields(code):
    """Verify metadata fields for primary agricultural languages."""
    info = get_language_info(code)
    assert info["code"] == code
    assert "name" in info
    assert "native" in info
    assert "bcp47" in info
    assert len(info["bcp47"]) > 0


def test_language_fallback_to_english():
    """Unknown language codes should fall back safely to English."""
    info = get_language_info("non_existent_code")
    assert info["code"] == "en"
    assert info["bcp47"] == "en-IN"


def test_multilingual_prompt_directive():
    """Verify prompt directives inject strict vernacular response rules."""
    hindi_directive = build_multilingual_prompt_directive("hi")
    assert "Hindi" in hindi_directive
    assert "Devanagari" in hindi_directive

    bengali_directive = build_multilingual_prompt_directive("bn")
    assert "Bengali" in bengali_directive
    assert "Bengali script" in bengali_directive

    english_directive = build_multilingual_prompt_directive("en")
    assert "English" in english_directive


def test_clean_markdown_for_speech():
    """Verify markdown bold, bullets, links, and units are sanitized for TTS audio readout."""
    raw = "**Dosage:** Apply *2.5 ml* of Mancozeb @ 75% per litre.\n- First action: check soil moisture."
    cleaned = clean_markdown_for_speech(raw)
    assert "**" not in cleaned
    assert "*" not in cleaned
    assert "@" not in cleaned
    assert "percent" in cleaned
    assert "Mancozeb" in cleaned


def test_api_voice_languages():
    """Test /api/voice/languages endpoint."""
    response = client.get("/api/voice/languages")
    assert response.status_code == 200
    data = response.json()
    assert data["total_languages"] == 23
    assert len(data["languages"]) == 23
    assert "hi" in data["languages"]
    assert "bn" in data["languages"]


def test_api_voice_format_speech():
    """Test /api/voice/format-speech endpoint."""
    payload = {
        "text": "**Tomato Blight:** Spray Copper Oxychloride @ 0.3% immediately.",
        "language": "hi",
    }
    response = client.post("/api/voice/format-speech", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["language_name"] == "Hindi"
    assert data["bcp47_code"] == "hi-IN"
    assert "**" not in data["speakable_text"]


def test_api_chat_with_multilingual_parameter():
    """Test /api/chat/message accepts language parameter without errors."""
    payload = {
        "message": "What is the spray dose for Tomato Early Blight?",
        "language": "hi",
    }
    response = client.post("/api/chat/message", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "reply" in data
    assert len(data["reply"]) > 0
    # Technical leakage check: response must not contain internal tech jargon
    assert "ExecuTorch" not in data["reply"]
    assert "GGUF" not in data["reply"]
    assert "embedding" not in data["reply"].lower()


def test_bengali_chat_and_vision_100_percent_localized():
    """
    Verify that when Bengali ('bn') is selected:
    1. Chat advisory for Rice Leaf Roller and Tomato Early Blight returns 100% Bengali text
       with zero untranslated English headers ('Target Pest:', 'Economic Threshold Level')
       and includes detailed fungicide/insecticide dosage and how/when to apply.
    2. Vision sample analysis and Pest sample analysis return localized Bengali fields.
    """
    # 1. Bengali Chat Advisory for Rice Leaf Roller
    chat_resp = client.post(
        "/api/chat/message",
        json={
            "message": "How to treat Pest Infestation in Rice Leaf Roller / Folder (Cnaphalocrocis medinalis)?",
            "language": "bn",
        },
    )
    assert chat_resp.status_code == 200
    reply_bn = chat_resp.json()["reply"]
    assert "নমস্কার কৃষক ভাই" in reply_bn
    assert "কখন ও কীভাবে প্রয়োগ করবেন" in reply_bn
    assert "Target Pest:" not in reply_bn
    assert "Economic Threshold Level (ETL):" not in reply_bn
    assert "Organic Bio-Control Remedy:" not in reply_bn
    for src in chat_resp.json()["sources"]:
        assert "**" not in src

    # 2. Bengali Disease Scanner Sample
    disease_resp = client.post("/api/vision/analyze-sample/tomato_early_blight.jpg?lang=bn")
    assert disease_resp.status_code == 200
    d_data = disease_resp.json()
    assert "টমেটো" in d_data["crop_name"]
    assert "আগাম ধসা" in d_data["detected_condition"]
    assert any("ছত্রাকনাশক" in act for act in d_data["recommended_action"])
    assert any("কখন ও কীভাবে" in act for act in d_data["recommended_action"])

    # 3. Bengali Pest Scanner Sample
    pest_resp = client.post("/api/vision/analyze-pest-sample/pest_rice_leaf_roller.jpg?lang=bn")
    assert pest_resp.status_code == 200
    p_data = pest_resp.json()
    det0 = p_data["detections"][0]
    assert "পাতা মোড়ানো পোকা" in det0["pest_name"]
    assert "গোছায়" in det0["action_threshold"]
    assert "ট্রাইকোগ্রামা" in det0["organic_remedy"]
    assert "প্রয়োগ বিধি" in det0["chemical_remedy"]
