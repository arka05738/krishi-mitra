"""
Pydantic API Schemas module for Krishi Mitra Offline Server.
"""
from server.app.schemas.api_models import (
    CropAnalysisResult,
    SampleImageInfo,
    SampleImagesResponse,
    AdvisoryQueryRequest,
    AdvisoryResult,
    SoilReportInput,
    SoilReportOutput,
    ChatRequest,
    ChatResponse,
    SystemHealthResponse,
    SystemStatusResponse,
)

__all__ = [
    "CropAnalysisResult",
    "SampleImageInfo",
    "SampleImagesResponse",
    "AdvisoryQueryRequest",
    "AdvisoryResult",
    "SoilReportInput",
    "SoilReportOutput",
    "ChatRequest",
    "ChatResponse",
    "SystemHealthResponse",
    "SystemStatusResponse",
]
