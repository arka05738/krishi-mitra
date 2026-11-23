"""
Application Configuration and Strict Offline Environment Settings.
Enforces zero outbound internet access and local network binding.
"""
import os
import socket
from pathlib import Path
from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict

# Enforce strict offline execution before importing any machine learning libraries if not configured
os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

# Directory layout anchors
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
SERVER_DIR = PROJECT_ROOT / "server"
CLIENT_DIR = PROJECT_ROOT / "client"
CLIENT_DIST_DIR = CLIENT_DIR / "dist"
CHROMA_PERSIST_DIR = SERVER_DIR / "chroma_db"
KNOWLEDGE_BASE_PATH = PROJECT_ROOT / "Advisory data" / "india_farmer_advisory_rag_knowledge_base.md"
SAMPLE_IMAGES_DIR = Path(__file__).resolve().parent / "vision" / "sample_images"


def get_local_ip() -> str:
    """Best-effort detection of local Wi-Fi hotspot IP address for edge client access."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Using dummy non-routable address to discover default interface IP without sending packets
        s.connect(("192.168.31.255", 9))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "192.168.31.235"


class Settings(BaseSettings):
    """Configuration settings for Krishi Mitra Offline Agricultural Server."""

    APP_NAME: str = "Krishi Mitra Agricultural Advisory Server"
    APP_VERSION: str = "1.0.0"
    
    # Network host & port binding (0.0.0.0 binds to all interfaces for Raspberry Pi access)
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = False
    WORKERS: int = 1
    LOG_LEVEL: str = "info"

    # Offline CORS Configuration (Permissive for local hotspot clients)
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]

    # File paths
    PROJECT_ROOT: Path = PROJECT_ROOT
    SERVER_DIR: Path = SERVER_DIR
    STATIC_DIST_DIR: Path = CLIENT_DIST_DIR
    CHROMA_PERSIST_DIR: Path = CHROMA_PERSIST_DIR
    KNOWLEDGE_BASE_PATH: Path = KNOWLEDGE_BASE_PATH
    SAMPLE_IMAGES_DIR: Path = SAMPLE_IMAGES_DIR

    # Local Ollama LLM Service (Optimized for 4GB Raspberry Pi 5)
    OLLAMA_BASE_URL: str = "http://127.0.0.1:11434"
    OLLAMA_MODEL: str = "llama3.2:1b"

    # Request limits
    MAX_UPLOAD_SIZE: int = 30 * 1024 * 1024  # 30 Megabytes

    # Farmer Helpline
    HELPLINE: str = "Kisan Call Centre: 1800-180-1551"
    
    # Edge hotspot IP
    EDGE_HOST_IP: str = get_local_ip()

    model_config = SettingsConfigDict(env_file=".env", extra="allow")


@lru_cache()
def get_settings() -> Settings:
    """Returns singleton cached instance of application settings."""
    return Settings()
