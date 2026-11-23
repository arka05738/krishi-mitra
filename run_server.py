"""
Root entrypoint for Krishi Mitra Offline Advisory Server.
Delegates to server/run_server.py.
"""
import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from server.run_server import main

if __name__ == "__main__":
    main()
