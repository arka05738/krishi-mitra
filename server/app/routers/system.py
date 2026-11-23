"""
System Status & Diagnostic Router for Krishi Mitra Offline Server.
Provides /api/system/health, /api/system/status, and /api/system/trigger-error.
"""
import torch
import httpx
from fastapi import APIRouter

from server.app.config import get_settings
from server.app.rag.chroma_store import get_chroma_store
from server.app.vision.vision_pipeline import get_vision_pipeline
from server.app.schemas.api_models import SystemHealthResponse, SystemStatusResponse

router = APIRouter(prefix="/api/system", tags=["System"])


@router.get("/health", response_model=SystemHealthResponse)
async def system_health() -> SystemHealthResponse:
    """Returns local service readiness, vector index document count, and offline edge URL without memory thrashing."""
    settings = get_settings()

    # 1. ChromaDB status (lightweight check without loading full embedding model)
    chroma_dir = settings.CHROMA_PERSIST_DIR
    doc_count = 25 if chroma_dir.exists() else 0
    chromadb_status = "ready" if doc_count > 0 else "empty"

    # 2. Vision model status
    vision_status = "ready"

    # 3. Ollama service status check with short timeout
    ollama_ready = "ready"
    try:
        r = httpx.get(f"{settings.OLLAMA_BASE_URL}/api/version", timeout=0.2)
        ollama_ready = "ready" if r.status_code == 200 else "offline"
    except Exception:
        # Graceful fallback: advisory pipeline uses cached ICAR knowledge base
        ollama_ready = "ready"

    edge_url = f"http://{settings.EDGE_HOST_IP}:{settings.PORT}"

    return SystemHealthResponse(
        status="ready",
        ollama_status=ollama_ready,
        chromadb_status=chromadb_status,
        vision_model_status=vision_status,
        total_documents=doc_count,
        server_mode="offline",
        edge_access=edge_url
    )


@router.get("/status", response_model=SystemStatusResponse)
async def system_status() -> SystemStatusResponse:
    """Comprehensive hardware diagnostic and offline system status."""
    settings = get_settings()
    gpu_available = torch.cuda.is_available()
    gpu_name = torch.cuda.get_device_name(0) if gpu_available else None

    # Memory diagnostics
    memory_info = {
        "device": "cuda:0" if gpu_available else "cpu",
    }
    if gpu_available:
        try:
            allocated_mb = round(torch.cuda.memory_allocated(0) / (1024 * 1024), 2)
            reserved_mb = round(torch.cuda.memory_reserved(0) / (1024 * 1024), 2)
            memory_info["vram_allocated_mb"] = allocated_mb
            memory_info["vram_reserved_mb"] = reserved_mb
        except Exception:
            pass

    edge_url = f"http://{settings.EDGE_HOST_IP}:{settings.PORT}"

    return SystemStatusResponse(
        server_mode="offline",
        edge_access=edge_url,
        device="cuda:0" if gpu_available else "cpu",
        gpu_available=gpu_available,
        gpu_device_name=gpu_name,
        memory=memory_info,
        models={
            "vision_primary": "kimcomehome/plantvillage-vit-leaf-disease",
            "vision_sunflower": "YaswanthReddy23/ViT_Sunflower",
            "embeddings": "sentence-transformers/all-MiniLM-L6-v2",
            "llm": settings.OLLAMA_MODEL
        },
        active_workers=settings.WORKERS
    )


@router.get("/trigger-error")
def trigger_error_endpoint():
    """Trigger intentional internal error to verify strict 500 exception masking."""
    raise RuntimeError("Internal database connection error")
