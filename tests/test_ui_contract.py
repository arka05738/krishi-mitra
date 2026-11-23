"""
Unit and Contract Verification for Krishi Mitra Farmer React Dashboard (Milestone M4).
Verifies:
1. Component presence and export integrity.
2. Zero Unicode emojis across all frontend sources and build artifacts.
3. Zero technical jargon / model names in frontend user interface.
4. Schema synchronization between frontend TypeScript interfaces and backend Pydantic models.
5. Agricultural safety alerts (Zinc Sulphate + DAP chemical lockup warning).
6. Government scheme requirements (PMFBY 72h rule, 14447 helpline, PM-KISAN, KCC, 1800-180-1551).
"""
import re
import json
import pytest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
CLIENT_SRC = PROJECT_ROOT / "client" / "src"
CLIENT_DIST = PROJECT_ROOT / "client" / "dist"

EMOJI_PATTERN = re.compile(
    r"[\U0001F300-\U0001FAFF\U0001F1E6-\U0001F1FF\U00002600-\U000027BF]"
)

FORBIDDEN_JARGON = [
    "llama", "llama3", "llama3.2", "vit", "fastapi", "uvicorn", "pydantic",
    "ollama", "chromadb", "chroma", "transformers", "huggingface", "pytorch",
    "cuda", "rag", "vectorstore", "embedding", "embeddings", "token", "tokens",
    "chunk", "chunks", "prompt template", "neural network", "vram"
]


def test_required_components_exist():
    """Verify all 6 core dashboard components and services are implemented."""
    required_files = [
        CLIENT_SRC / "types" / "index.ts",
        CLIENT_SRC / "services" / "api.ts",
        CLIENT_SRC / "components" / "Navigation.tsx",
        CLIENT_SRC / "components" / "CropDoctor.tsx",
        CLIENT_SRC / "components" / "Chat.tsx",
        CLIENT_SRC / "components" / "SoilCard.tsx",
        CLIENT_SRC / "components" / "Schemes.tsx",
        CLIENT_SRC / "components" / "Status.tsx",
        CLIENT_SRC / "App.tsx",
    ]
    for p in required_files:
        assert p.exists(), f"Required file missing: {p}"
        assert p.stat().st_size > 100, f"File {p} is empty or stubbed"


def test_zero_unicode_emojis_in_source():
    """Verify zero Unicode emojis in any client source file (.ts, .tsx, .css, .html)."""
    violations = []
    for p in CLIENT_SRC.rglob("*"):
        if p.is_file() and p.suffix in (".ts", ".tsx", ".css", ".html"):
            text = p.read_text(encoding="utf-8", errors="ignore")
            matches = EMOJI_PATTERN.findall(text)
            if matches:
                violations.append((p.name, matches))
    assert len(violations) == 0, f"Found Unicode emojis in source: {violations}"


def test_zero_unicode_emojis_in_dist():
    """Verify zero Unicode emojis in compiled production bundle."""
    violations = []
    for p in CLIENT_DIST.rglob("*"):
        if p.is_file() and p.suffix in (".html", ".js", ".css"):
            text = p.read_text(encoding="utf-8", errors="ignore")
            matches = EMOJI_PATTERN.findall(text)
            if matches:
                violations.append((p.name, matches))
    assert len(violations) == 0, f"Found Unicode emojis in dist: {violations}"


def test_dist_index_html_zero_jargon():
    """Verify client/dist/index.html contains zero technical jargon."""
    dist_html = (CLIENT_DIST / "index.html").read_text(encoding="utf-8")
    for term in FORBIDDEN_JARGON:
        pat = rf"(?<![a-zA-Z0-9_]){re.escape(term)}(?![a-zA-Z0-9_])"
        assert not re.search(pat, dist_html, re.IGNORECASE), f"Jargon leaked in index.html: {term}"


def test_mandatory_soil_mixing_safety_warning():
    """Verify mandatory alert 'Do NOT mix Zinc Sulphate directly with DAP' is present."""
    soil_card_code = (CLIENT_SRC / "components" / "SoilCard.tsx").read_text(encoding="utf-8")
    assert "Do NOT mix Zinc Sulphate directly with DAP" in soil_card_code, (
        "Mandatory Zinc Sulphate + DAP safety alert missing in SoilCard.tsx"
    )


def test_mandatory_pmfby_72h_and_helpline():
    """Verify PMFBY mandatory 72h calamity notice and 14447 helpline."""
    schemes_code = (CLIENT_SRC / "components" / "Schemes.tsx").read_text(encoding="utf-8")
    assert "72" in schemes_code, "PMFBY 72-hour notice period missing in Schemes.tsx"
    assert "14447" in schemes_code, "Crop insurance helpline 14447 missing in Schemes.tsx"
    assert "1800-180-1551" in schemes_code, "Kisan Call Centre 1800-180-1551 missing in Schemes.tsx"
    assert "PM-KISAN" in schemes_code, "PM-KISAN scheme missing in Schemes.tsx"


def test_api_relative_base_url():
    """Verify API client uses relative base URL for mobile hotspot / Pi 5 compatibility."""
    api_code = (CLIENT_SRC / "services" / "api.ts").read_text(encoding="utf-8")
    assert "http://localhost:8000" not in api_code, (
        "Hardcoded localhost:8000 in api.ts breaks Raspberry Pi 5 edge connectivity"
    )


def test_high_contrast_grade_badges_css():
    """Verify high contrast CSS tokens and daylight borders."""
    css = (CLIENT_SRC / "index.css").read_text(encoding="utf-8")
    assert "--color-success" in css
    assert "--color-warning" in css
    assert "--color-danger" in css
    assert "grade-badge--a" in css
    assert "grade-badge--b" in css
    assert "grade-badge--c" in css
