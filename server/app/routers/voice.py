"""
Voice Assistant Router for Multilingual Farmer Speech Interaction.
Powered by offline Hugging Face Whisper-tiny for STT and Web Speech API / TTS bridge.
Supports 22 Scheduled Indian Languages + English.
"""

import os
import io
import re
import tempfile
import logging
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel

from server.app.rag.multilingual import INDIC_LANGUAGES

logger = logging.getLogger("voice_router")
router = APIRouter(prefix="/api/voice", tags=["Voice Assistant"])

_whisper_pipeline = None

def get_whisper():
    """Lazy loader for offline Hugging Face Whisper ASR pipeline."""
    global _whisper_pipeline
    if _whisper_pipeline is None:
        from transformers import pipeline
        logger.info("Initializing offline Whisper-tiny ASR pipeline on CPU...")
        _whisper_pipeline = pipeline(
            "automatic-speech-recognition",
            model="openai/whisper-tiny",
            device="cpu"
        )
        logger.info("Whisper-tiny ASR pipeline online.")
    return _whisper_pipeline


class TranscriptionResponse(BaseModel):
    text: str
    language: Optional[str] = "en"
    success: bool = True


class SpeechTextRequest(BaseModel):
    text: str
    language: Optional[str] = "en"


class SpeechTextResponse(BaseModel):
    speakable_text: str
    bcp47_code: str
    language_name: str
    native_name: str


@router.get("/languages")
async def get_supported_languages() -> Dict[str, Any]:
    """Returns all 22 Scheduled Indian Languages + English with Speech codes."""
    return {
        "total_languages": len(INDIC_LANGUAGES),
        "languages": INDIC_LANGUAGES
    }


@router.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe_audio(
    file: UploadFile = File(...),
    language: Optional[str] = Form("hi")
) -> TranscriptionResponse:
    """
    Transcribes farmer voice audio using on-device Hugging Face Whisper-tiny.
    Supports .wav, .webm, .ogg, .mp3 audio uploads.
    """
    if not file:
        raise HTTPException(status_code=400, detail="No audio file provided")

    try:
        content = await file.read()
        if len(content) == 0:
            raise HTTPException(status_code=400, detail="Empty audio file")

        # Write to temporary file for Whisper processing
        suffix = os.path.splitext(file.filename or "")[1] or ".webm"
        with tempfile.NamedTemporaryFile(suffix=suffix, delete=False) as tmp:
            tmp.write(content)
            tmp_path = tmp.name

        try:
            asr = get_whisper()
            # Generate transcription
            target_lang = language.lower() if language and language.lower() in INDIC_LANGUAGES else "hi"
            lang_param = target_lang if target_lang not in ("en", "auto") else None

            gen_kwargs = {"max_new_tokens": 128}
            if lang_param:
                gen_kwargs["language"] = lang_param

            result = await asyncio.wait_for(
                asyncio.to_thread(asr, tmp_path, generate_kwargs=gen_kwargs),
                timeout=12.0
            )
            transcribed_text = result.get("text", "").strip()

            return TranscriptionResponse(
                text=transcribed_text,
                language=target_lang,
                success=True
            )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Whisper transcription error: {e}")
        return TranscriptionResponse(
            text="",
            language=language or "en",
            success=False
        )


@router.post("/format-speech", response_model=SpeechTextResponse)
async def format_for_speech(req: SpeechTextRequest) -> SpeechTextResponse:
    """
    Cleans markdown formatting, symbols, and bullets from advisory text
    so TTS engines pronounce it smoothly and clearly for farmers.
    """
    raw = req.text
    # Remove markdown bold/italics
    clean = re.sub(r"\*\*([^*]+)\*\*", r"\1", raw)
    clean = re.sub(r"\*([^*]+)\*", r"\1", clean)
    # Remove markdown headers and bullets
    clean = re.sub(r"^[#\*\-•]+\s*", "", clean, flags=re.MULTILINE)
    # Replace slashes and percentages with verbal equivalents
    clean = clean.replace("@", " at ").replace("\\%", " percent").replace("%", " percent")
    clean = re.sub(r"\s+", " ", clean).strip()

    lang_info = INDIC_LANGUAGES.get(req.language.lower(), INDIC_LANGUAGES["en"])
    return SpeechTextResponse(
        speakable_text=clean,
        bcp47_code=lang_info["bcp47"],
        language_name=lang_info["name"],
        native_name=lang_info["native"]
    )
