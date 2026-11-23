# Vision package initialization
"""
Offline Vision Pipeline Package.
Provides deep learning inference and farmer-friendly translation for crop & flower health assessment.
"""

from .label_mapper import (
    CropAnalysisResult,
    LabelMapper,
    map_prediction_to_result,
    LABEL_DATABASE
)
from .vision_pipeline import (
    VisionPipeline,
    get_vision_pipeline,
    analyze_crop_image
)
from .sample_generator import (
    generate_all_sample_images
)

__all__ = [
    "CropAnalysisResult",
    "LabelMapper",
    "map_prediction_to_result",
    "LABEL_DATABASE",
    "VisionPipeline",
    "get_vision_pipeline",
    "analyze_crop_image",
    "generate_all_sample_images",
]
