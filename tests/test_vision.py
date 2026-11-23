# Milestone M1 Unit and Integration Test Suite: Offline Vision Pipeline
"""
Comprehensive tests for:
- 100% offline enforcement (no network access allowed)
- Model loading on CUDA/CPU and inference
- LabelMapper coverage across all 38 PlantVillage + 4 Sunflower classes
- Quality grade calculations and boundaries
- Farmer-friendly jargon check (zero model/tech leaks)
- Sample image generation and inference across file path, PIL Image, and bytes
- Schema validation of CropAnalysisResult
"""

import os
import re
import socket
from pathlib import Path
from typing import Set

import pytest
from PIL import Image

# Ensure project root is in sys.path
import sys
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from server.app.vision.label_mapper import (
    CropAnalysisResult,
    LabelMapper,
    map_prediction_to_result,
    LABEL_DATABASE,
)
from server.app.vision.vision_pipeline import (
    VisionPipeline,
    get_vision_pipeline,
    analyze_crop_image,
)
from server.app.vision.sample_generator import (
    generate_all_sample_images,
    DEFAULT_OUTPUT_DIR,
)


# =====================================================================
# 1. OFFLINE ENFORCEMENT TESTS
# =====================================================================

def test_offline_environment_variables():
    """Verify that offline environment variables are strictly set."""
    assert os.environ.get("HF_HUB_OFFLINE") == "1", "HF_HUB_OFFLINE must be 1"
    assert os.environ.get("TRANSFORMERS_OFFLINE") == "1", "TRANSFORMERS_OFFLINE must be 1"


def test_zero_network_during_inference(monkeypatch, tmp_path):
    """
    Verify that inference executes without making any network calls.
    Monkeypatches socket.socket.connect to raise an error if invoked.
    """
    def forbidden_connect(self, *args, **kwargs):
        raise RuntimeError("Integrity Violation: Outbound network call attempted during offline inference!")

    monkeypatch.setattr(socket.socket, "connect", forbidden_connect)

    pipeline = get_vision_pipeline()
    test_img = Image.new("RGB", (224, 224), color=(34, 139, 34))

    # Should run 100% offline without triggering socket.connect
    res = pipeline.analyze(test_img)
    assert isinstance(res, CropAnalysisResult)
    assert res.crop_name != ""


# =====================================================================
# 2. MODEL LOADING & INFERENCE TESTS
# =====================================================================

def test_pipeline_device_and_models():
    """Verify VisionPipeline loads successfully with appropriate compute device."""
    pipeline = get_vision_pipeline()
    assert pipeline.device.type in ("cuda", "cpu")
    # Verify primary model loaded offline
    proc, model = pipeline._get_or_load_model(pipeline.primary_model_id)
    assert len(model.config.id2label) == 38, f"Expected 38 PlantVillage classes, got {len(model.config.id2label)}"


def test_sunflower_routing():
    """Verify that crop_hint routing correctly loads and uses the sunflower model."""
    pipeline = get_vision_pipeline()
    test_img = Image.new("RGB", (224, 224), color=(255, 215, 0))

    # Without hint -> primary model
    raw_primary = pipeline.predict_raw(test_img)
    assert raw_primary["model_id"] == pipeline.primary_model_id

    # With sunflower hint -> sunflower model
    raw_sunflower = pipeline.predict_raw(test_img, crop_hint="sunflower")
    assert raw_sunflower["model_id"] == pipeline.sunflower_model_id
    assert raw_sunflower["predicted_label"] in ["Healthy", "Downy mildew", "Gray mold", "Leaf scars"]


def test_inference_input_formats():
    """Verify pipeline accepts file path (str & Path), PIL Image, and raw bytes."""
    pipeline = get_vision_pipeline()

    # PIL Image
    pil_img = Image.new("RGB", (224, 224), color=(40, 160, 40))
    res_pil = pipeline.analyze(pil_img)
    assert isinstance(res_pil, CropAnalysisResult)

    # Raw bytes
    import io
    byte_io = io.BytesIO()
    pil_img.save(byte_io, format="JPEG")
    raw_bytes = byte_io.getvalue()
    res_bytes = pipeline.analyze(raw_bytes)
    assert isinstance(res_bytes, CropAnalysisResult)
    assert res_bytes.crop_name == res_pil.crop_name

    # Path object
    sample_file = DEFAULT_OUTPUT_DIR / "tomato_healthy.jpg"
    if sample_file.exists():
        res_path = pipeline.analyze(sample_file)
        assert isinstance(res_path, CropAnalysisResult)
        # String path
        res_str = pipeline.analyze(str(sample_file))
        assert isinstance(res_str, CropAnalysisResult)


# =====================================================================
# 3. LABEL MAPPER ACCURACY & QUALITY GRADING TESTS
# =====================================================================

PLANTVILLAGE_38_CLASSES = [
    "Apple___Apple_scab",
    "Apple___Black_rot",
    "Apple___Cedar_apple_rust",
    "Apple___healthy",
    "Blueberry___healthy",
    "Cherry_(including_sour)___Powdery_mildew",
    "Cherry_(including_sour)___healthy",
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot",
    "Corn_(maize)___Common_rust_",
    "Corn_(maize)___Northern_Leaf_Blight",
    "Corn_(maize)___healthy",
    "Grape___Black_rot",
    "Grape___Esca_(Black_Measles)",
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)",
    "Grape___healthy",
    "Orange___Haunglongbing_(Citrus_greening)",
    "Peach___Bacterial_spot",
    "Peach___healthy",
    "Pepper,_bell___Bacterial_spot",
    "Pepper,_bell___healthy",
    "Potato___Early_blight",
    "Potato___Late_blight",
    "Potato___healthy",
    "Raspberry___healthy",
    "Soybean___healthy",
    "Squash___Powdery_mildew",
    "Strawberry___Leaf_scorch",
    "Strawberry___healthy",
    "Tomato___Bacterial_spot",
    "Tomato___Early_blight",
    "Tomato___Late_blight",
    "Tomato___Leaf_Mold",
    "Tomato___Septoria_leaf_spot",
    "Tomato___Spider_mites Two-spotted_spider_mite",
    "Tomato___Target_Spot",
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
    "Tomato___Tomato_mosaic_virus",
    "Tomato___healthy"
]

SUNFLOWER_4_CLASSES = [
    "Downy mildew",
    "Gray mold",
    "Healthy",
    "Leaf scars"
]


def test_label_mapper_covers_all_plantvillage_classes():
    """Verify all 38 PlantVillage classes map to complete, valid CropAnalysisResults."""
    for raw_label in PLANTVILLAGE_38_CLASSES:
        res = LabelMapper.get_mapping(raw_label, confidence=0.92)
        assert res.crop_name != "", f"Empty crop_name for {raw_label}"
        assert res.detected_condition != "", f"Empty condition for {raw_label}"
        assert res.quality_grade in ["Grade A (Prime)", "Grade B (Early Attention)", "Grade C (Health Risk)"]
        assert 0 <= res.quality_score <= 100, f"Invalid score {res.quality_score} for {raw_label}"
        assert res.severity in ["None", "Mild", "Moderate", "Critical"]
        assert len(res.recommended_action) >= 2, f"Too few actions for {raw_label}"
        assert len(res.summary.strip()) > 20, f"Summary too short for {raw_label}"


def test_label_mapper_covers_all_sunflower_classes():
    """Verify all 4 Sunflower classes map cleanly with crop_hint."""
    for raw_label in SUNFLOWER_4_CLASSES:
        res = LabelMapper.get_mapping(raw_label, confidence=0.88, crop_hint="sunflower")
        assert res.crop_name == "Sunflower"
        assert res.detected_condition != ""
        assert res.quality_grade in ["Grade A (Prime)", "Grade B (Early Attention)", "Grade C (Health Risk)"]
        assert 0 <= res.quality_score <= 100
        assert len(res.recommended_action) >= 2


def test_quality_grading_tiers():
    """
    Verify quality grading tier rules:
    - Grade A (Prime / Healthy): score 85-100%, severity None
    - Grade B (Early Attention / Mild): score 50-84%, severity Mild or Moderate
    - Grade C (Health Risk / Critical): score 0-49%, severity Critical
    """
    # 1. Healthy instances
    healthy_classes = [
        "Tomato___healthy",
        "Apple___healthy",
        "Potato___healthy",
        "Corn_(maize)___healthy",
        "Strawberry___healthy",
        "Sunflower___Healthy"
    ]
    for cls_name in healthy_classes:
        res = LabelMapper.get_mapping(cls_name, confidence=0.95)
        assert res.quality_grade == "Grade A (Prime)", f"{cls_name} should be Grade A"
        assert res.severity == "None", f"{cls_name} severity should be None"
        assert 85 <= res.quality_score <= 100, f"{cls_name} score {res.quality_score} should be >= 85"

    # 2. Critical blight / viral instances
    critical_classes = [
        "Potato___Late_blight",
        "Tomato___Late_blight",
        "Tomato___Tomato_Yellow_Leaf_Curl_Virus",
        "Orange___Haunglongbing_(Citrus_greening)",
        "Sunflower___Downy_mildew"
    ]
    for cls_name in critical_classes:
        res = LabelMapper.get_mapping(cls_name, confidence=0.95)
        assert res.quality_grade == "Grade C (Health Risk)", f"{cls_name} should be Grade C"
        assert res.severity == "Critical", f"{cls_name} severity should be Critical"
        assert 0 <= res.quality_score <= 49, f"{cls_name} score {res.quality_score} should be <= 49"

    # 3. Mild / Moderate attention instances
    mild_classes = [
        "Tomato___Early_blight",
        "Corn_(maize)___Common_rust_",
        "Apple___Apple_scab",
        "Sunflower___Leaf_scars"
    ]
    for cls_name in mild_classes:
        res = LabelMapper.get_mapping(cls_name, confidence=0.95)
        assert res.quality_grade == "Grade B (Early Attention)", f"{cls_name} should be Grade B"
        assert res.severity in ["Mild", "Moderate"], f"{cls_name} severity should be Mild or Moderate"
        assert 50 <= res.quality_score <= 84, f"{cls_name} score {res.quality_score} should be in 50-84"


def test_confidence_scaling():
    """Verify that confidence modulates quality scores within legal grade ranges."""
    low_conf_healthy = LabelMapper.get_mapping("Tomato___healthy", confidence=0.5)
    high_conf_healthy = LabelMapper.get_mapping("Tomato___healthy", confidence=0.99)
    assert 85 <= low_conf_healthy.quality_score <= 100
    assert 85 <= high_conf_healthy.quality_score <= 100
    assert high_conf_healthy.quality_score >= low_conf_healthy.quality_score


# =====================================================================
# 4. ZERO JARGON AUDIT
# =====================================================================

PROHIBITED_JARGON: Set[str] = {
    "vit",
    "vision transformer",
    "transformer",
    "huggingface",
    "hugging face",
    "pytorch",
    "torch",
    "softmax",
    "neural network",
    "deep learning",
    "convolution",
    "cnn",
    "tensor",
    "classification",
    "classifier",
    "confidence score",
    "plantvillage",
    "model weights",
    "logits",
    "backpropagation",
    "dataset"
}


def test_farmer_terminology_zero_jargon():
    """
    Audit all class translations in LABEL_DATABASE to ensure ZERO technical jargon leaks
    into farmer summaries or recommended remedial actions.
    """
    for key, data in LABEL_DATABASE.items():
        text_corpus = (
            data["summary"] + " " + " ".join(data["recommended_action"])
        ).lower()

        # Word boundary check for prohibited keywords
        for jargon in PROHIBITED_JARGON:
            pattern = rf"\b{re.escape(jargon)}\b"
            assert not re.search(pattern, text_corpus), (
                f"JARGON LEAK DETECTED in '{key}': found '{jargon}' in text:\n'{text_corpus}'"
            )


# =====================================================================
# 5. SAMPLE GENERATOR & TEST FIXTURES
# =====================================================================

EXPECTED_SAMPLE_FILES = [
    "tomato_healthy.jpg",
    "tomato_early_blight.jpg",
    "potato_late_blight.jpg",
    "sunflower_healthy.jpg",
    "corn_common_rust.jpg",
    "apple_scab.jpg"
]


def test_sample_image_generator_produces_valid_files():
    """Verify sample_generator creates all 6 realistic RGB sample images."""
    paths = generate_all_sample_images()
    assert len(paths) == 6

    for filename in EXPECTED_SAMPLE_FILES:
        target_path = DEFAULT_OUTPUT_DIR / filename
        assert target_path.exists(), f"Missing sample image: {target_path}"
        assert target_path.stat().st_size > 5000, f"Sample image file too small: {target_path}"

        # Verify image integrity with PIL
        with Image.open(target_path) as img:
            assert img.format == "JPEG"
            assert img.mode == "RGB"
            assert img.size[0] >= 256 and img.size[1] >= 256


def test_end_to_end_inference_on_sample_images():
    """Run pipeline end-to-end on each generated sample image file."""
    for filename in EXPECTED_SAMPLE_FILES:
        img_path = DEFAULT_OUTPUT_DIR / filename
        assert img_path.exists()
        crop_hint = "sunflower" if "sunflower" in filename else None
        res = analyze_crop_image(img_path, crop_hint=crop_hint)

        assert isinstance(res, CropAnalysisResult)
        assert len(res.crop_name) > 0
        assert len(res.detected_condition) > 0
        assert 0 <= res.quality_score <= 100
        assert 0.0 <= res.confidence <= 1.0
        assert len(res.recommended_action) >= 2


# =====================================================================
# 6. PYDANTIC SCHEMA VALIDATION
# =====================================================================

def test_crop_analysis_result_schema_validation():
    """Validate CropAnalysisResult Pydantic schema serialization and field constraints."""
    data = {
        "crop_name": "Tomato",
        "detected_condition": "Early Blight (Leaf Spots)",
        "quality_grade": "Grade B (Early Attention)",
        "quality_score": 65,
        "confidence": 0.9412,
        "severity": "Moderate",
        "summary": "Foliage exhibits concentric dark rings. Early pruning preserves fruit yield.",
        "recommended_action": [
            "Prune infected lower foliage.",
            "Apply protective copper oxychloride spray.",
            "Avoid overhead leaf wetting."
        ]
    }
    result = CropAnalysisResult(**data)
    assert result.quality_score == 65
    assert result.confidence == 0.9412

    # Verify dict and json serialization
    d = result.model_dump() if hasattr(result, "model_dump") else result.dict()
    assert d["crop_name"] == "Tomato"
    assert len(d["recommended_action"]) == 3

    # Out of range test: quality_score > 100 should raise ValidationError
    with pytest.raises(Exception):
        CropAnalysisResult(**{**data, "quality_score": 120})

    # Out of range test: confidence > 1.0 should raise ValidationError
    with pytest.raises(Exception):
        CropAnalysisResult(**{**data, "confidence": 1.5})


# =====================================================================
# 7. TWO-STAGE CROP GATEKEEPER & QUALITY VERIFICATION
# =====================================================================

def test_crop_gatekeeper_detection_and_rejection():
    """
    Verify two-stage vision pipeline:
    1st: Check if picture is an agricultural crop or not (rejects non-crops).
    2nd: If yes, classify the crop automatically and evaluate quality & condition.
    """
    pipeline = get_vision_pipeline()

    # 1. Genuine crop image: Tomato / Plant sample
    sample_crop = DEFAULT_OUTPUT_DIR / "tomato_healthy.jpg"
    if sample_crop.exists():
        res_crop = pipeline.analyze(sample_crop)
        assert res_crop.is_crop is True, "Genuine plant leaf should be recognized as crop"
        assert len(res_crop.crop_name) > 0
        assert res_crop.quality_grade in ["Grade A (Prime)", "Grade B (Early Attention)", "Grade C (Health Risk)"]

    # 2. Non-crop image (non_leaf.jpg)
    non_leaf_path = PROJECT_ROOT / "tests" / "test_fixtures" / "images" / "non_leaf.jpg"
    if non_leaf_path.exists():
        res_non_crop = pipeline.analyze(non_leaf_path)
        assert res_non_crop.is_crop is False, "Non-leaf image should be rejected by gatekeeper"
        assert res_non_crop.crop_name == "Not a Crop or Plant"
        assert res_non_crop.quality_grade == "Not Applicable"
        assert res_non_crop.quality_score == 0
        assert "No crop" in res_non_crop.summary or "No agricultural crop" in res_non_crop.summary

    # 3. Pure black / flat non-crop image
    black_img = Image.new("RGB", (224, 224), color=(0, 0, 0))
    res_black = pipeline.analyze(black_img)
    assert res_black.is_crop is False, "Pure black image should be rejected as non-crop"
    assert res_black.crop_name == "Not a Crop or Plant"

