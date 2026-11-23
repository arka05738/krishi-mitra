"""
Offline RAG Advisory Engine and Soil Health Card Diagnostic Module.
"""

from .knowledge_ingestion import (
    KnowledgeChunk,
    KnowledgeBaseChunker,
    clean_agronomic_text,
    parse_knowledge_base,
    ingest_knowledge_base,
)

from .chroma_store import (
    LocalMiniLMEmbeddingFunction,
    ChromaStore,
    get_chroma_store,
)

from .soil_calculator import (
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

from .rag_pipeline import (
    AdvisoryResult,
    RAGPipeline,
    RagPipeline,
    FARMER_SYSTEM_PROMPT,
    FARMER_PROMPT_TEMPLATE,
)

__all__ = [
    "KnowledgeChunk",
    "KnowledgeBaseChunker",
    "clean_agronomic_text",
    "parse_knowledge_base",
    "ingest_knowledge_base",
    "LocalMiniLMEmbeddingFunction",
    "ChromaStore",
    "get_chroma_store",
    "SoilReportInput",
    "SoilReportOutput",
    "calculate_soil_health",
    "calculate_fertilizer_recommendation",
    "classify_soil_ph",
    "classify_ec",
    "classify_oc",
    "classify_primary_nutrient",
    "get_crop_profile",
    "CROP_DATABASE",
    "AdvisoryResult",
    "RAGPipeline",
    "RagPipeline",
    "FARMER_SYSTEM_PROMPT",
    "FARMER_PROMPT_TEMPLATE",
]
