"""
FastAPI Server Application Factory for Krishi Mitra Offline Agricultural System.
Configures CORS, routers, static frontend distribution, lifespan preloading,
and strict farmer-safe exception masking.
"""
import os
import sys
from pathlib import Path
from contextlib import asynccontextmanager

# Enforce strict 100% offline mode before any ML framework imports if not configured
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

from fastapi import FastAPI, Request, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles

from server.app.config import get_settings
from server.app.routers import vision, advisory, chat, system, voice
from server.app.vision.vision_pipeline import get_vision_pipeline
from server.app.rag.chroma_store import get_chroma_store


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan context manager for warm-up and preloading.
    Preloads Hugging Face ViT models into memory and verifies ChromaDB index.
    """
    settings = get_settings()
    print("=" * 65)
    print("  Krishi Mitra — Offline Agricultural Advisory Server")
    print("  Mode       : 100% Offline (Zero Outbound Network Dependency)")
    print(f"  Binding    : http://{settings.HOST}:{settings.PORT}")
    print(f"  Edge Hotspot : http://{settings.EDGE_HOST_IP}:{settings.PORT}")
    print(f"  Workers    : {settings.WORKERS}")
    print("=" * 65)

    is_render = os.getenv("RENDER") is not None
    if is_render:
        print("[Startup] Cloud container environment detected: ML pipelines set to on-demand lazy loading.")
    else:
        # 1. Warm-up vision pipeline
        try:
            pipeline = get_vision_pipeline()
            print(f"[Startup] Vision Pipeline initialized on device: {pipeline.device}")
        except Exception as e:
            print(f"[Startup Warning] Vision Pipeline preloading error: {e}")

        # 2. Warm-up ChromaStore vector database
        try:
            store = get_chroma_store()
            doc_count = store.count()
            print(f"[Startup] ChromaDB Vector Store online: {doc_count} knowledge chunks indexed")
        except Exception as e:
            print(f"[Startup Warning] ChromaDB initialization error: {e}")

    yield

    print("[Shutdown] Krishi Mitra Advisory Server terminated cleanly.")


def create_app() -> FastAPI:
    """Creates and configures the production FastAPI ASGI application."""
    settings = get_settings()

    app = FastAPI(
        title=settings.APP_NAME,
        version=settings.APP_VERSION,
        description="Offline local agricultural advisory backend for farmers",
        lifespan=lifespan,
    )

    # Permissive CORS for mobile Wi-Fi hotspot access (Raspberry Pi 5)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
        expose_headers=["*"],
    )

    # Register API Routers
    app.include_router(system.router)
    app.include_router(vision.router)
    app.include_router(advisory.router)
    app.include_router(chat.router)
    app.include_router(voice.router)

    # Static assets mounting for React frontend
    assets_dir = settings.STATIC_DIST_DIR / "assets"
    if assets_dir.exists():
        app.mount("/assets", StaticFiles(directory=str(assets_dir)), name="assets")

    # Explicit root routes serving index.html
    @app.get("/")
    @app.get("/index.html")
    async def serve_index():
        dist_html = settings.STATIC_DIST_DIR / "index.html"
        if dist_html.exists():
            return HTMLResponse(dist_html.read_text(encoding="utf-8"))
        return HTMLResponse('<!doctype html><html><body><div id="root"></div></body></html>')

    # Explicit HTTP exception handler ensuring exact client error codes
    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
            headers=exc.headers
        )

    # Global unhandled exception handler masking internal errors and stack traces
    @app.exception_handler(Exception)
    async def internal_server_error_handler(request: Request, exc: Exception):
        return JSONResponse(
            status_code=500,
            content={
                "detail": "Unable to process agricultural request. Please try again or contact Kisan Call Centre: 1800-180-1551"
            }
        )

    # Catch-all route for Single Page Application (SPA) client-side routing
    @app.get("/{full_path:path}")
    async def catch_all_spa_routes(full_path: str):
        # Strict 404 rejection for unknown /api/* requests (satisfies test_t2_1_2)
        if full_path.startswith("api/") or full_path == "api":
            raise HTTPException(status_code=404, detail="API route not found")

        # Check for static file in client/dist (e.g. favicon.svg, icons.svg)
        target_file = settings.STATIC_DIST_DIR / full_path
        if target_file.exists() and target_file.is_file():
            return FileResponse(str(target_file))

        # Fallback to SPA index.html
        dist_html = settings.STATIC_DIST_DIR / "index.html"
        if dist_html.exists():
            return HTMLResponse(dist_html.read_text(encoding="utf-8"))
        return HTMLResponse('<!doctype html><html><body><div id="root"></div></body></html>')

    return app


# Default ASGI application instance
app = create_app()
