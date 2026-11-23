"""
FastAPI routers package for Krishi Mitra server backend.
"""
from server.app.routers import vision, advisory, chat, system, voice

__all__ = ["vision", "advisory", "chat", "system", "voice"]
