"""
ExecuTorch Llama Microservice for Raspberry Pi 5 Edge Deployment.
Provides lightweight HTTP endpoint on localhost:8008 for on-device reasoning.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import uvicorn
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from llama_arm_runner import LlamaExecuTorchRunner

app = FastAPI(title="Krishi Mitra ExecuTorch Service", version="1.0.0")
runner = LlamaExecuTorchRunner()

class GenerationRequest(BaseModel):
    prompt: str
    system_prompt: Optional[str] = None
    language: Optional[str] = "en"

class GenerationResponse(BaseModel):
    response: str
    runtime: str
    hardware: str
    offline: bool

@app.post("/generate", response_model=GenerationResponse)
async def generate_advice(req: GenerationRequest):
    if not req.prompt:
        raise HTTPException(status_code=400, detail="Prompt is required")
    output = runner.generate(req.prompt, req.system_prompt, language=req.language or "en")
    metrics = runner.get_system_metrics()
    return GenerationResponse(
        response=output,
        runtime=metrics["runtime"],
        hardware=metrics["device"],
        offline=True
    )

@app.get("/status")
async def get_status():
    return runner.get_system_metrics()

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8008, log_level="info")
