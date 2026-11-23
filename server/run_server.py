"""
Standalone Startup Script for Krishi Mitra Advisory Server.
Binds to local Wi-Fi hotspot subnet for Raspberry Pi 5 edge access.
"""
import os
import sys
from pathlib import Path

# Enforce project root on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Enforce 100% offline flags before any ML framework imports
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import uvicorn
from server.app.config import get_settings


def main():
    settings = get_settings()
    print("=" * 65)
    print("  Krishi Mitra — Offline Agricultural Advisory Server")
    print("  Mode         : 100% Offline (Zero Outbound Network Dependency)")
    print(f"  Binding      : http://{settings.HOST}:{settings.PORT}")
    print(f"  Edge Hotspot : http://{settings.EDGE_HOST_IP}:{settings.PORT}")
    print(f"  Workers      : {settings.WORKERS}")
    print("=" * 65)

    uvicorn.run(
        "server.app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.RELOAD,
        workers=settings.WORKERS,
        log_level=settings.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
