"""
Pydantic API Schemas for Server Request and Response Payloads.
Zero technical jargon. Farmer-facing.
Strictly conforms to PROJECT.md interface contracts.
"""
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, model_validator


# =============================================================================
# 1. VISION API MODELS
# =============================================================================

class CropAnalysisResult(BaseModel):
    """Visual plant health analysis result conforming to PROJECT.md contract."""
    crop_name: str = Field(..., description="Target crop or flower entity name (e.g. Tomato, Sunflower)")
    detected_condition: str = Field(..., description="Condition or health state in farmer language")
    quality_grade: str = Field(..., description="Quality tier: Grade A (Prime), Grade B (Early Attention), Grade C (Health Risk)")
    quality_score: int = Field(..., ge=0, le=100, description="Overall health score (0-100)")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model prediction confidence (0.0-1.0)")
    severity: str = Field(..., description="Severity category: None, Mild, Moderate, Critical")
    summary: str = Field(..., description="Farmer-friendly summary with zero jargon")
    recommended_action: List[str] = Field(default_factory=list, description="Actionable step-by-step guidance points")
    is_crop: bool = Field(default=True, description="Whether image contains an agricultural crop, leaf, or flower")
    raw_label: Optional[str] = Field(default=None, description="Original model classification label for lossless language switching")


class SampleImageInfo(BaseModel):
    """Metadata for curated sample crop/flower images."""
    id: str = Field(..., description="Unique sample identifier")
    name: str = Field(..., description="Display title for farmer")
    filename: str = Field(..., description="Filename on disk")
    crop: str = Field(..., description="Crop or flower type")
    condition: str = Field(..., description="Health status description")
    url: str = Field(..., description="Static URL path to retrieve image")


class SampleImagesResponse(BaseModel):
    """List response for curated sample images."""
    samples: List[SampleImageInfo] = Field(default_factory=list)


# =============================================================================
# 2. ADVISORY & RAG API MODELS
# =============================================================================

class AdvisoryQueryRequest(BaseModel):
    """Farmer agricultural question submission."""
    query: Optional[str] = Field(None, description="Farmer agricultural query")
    question: Optional[str] = Field(None, description="Query alias for frontend compatibility")
    crop_name: Optional[str] = Field(None, description="Target crop context")
    vision_context: Optional[str] = Field(None, description="Optional vision diagnosis findings")
    language: Optional[str] = Field("en", description="Target 22 Indian language code")

    def get_query(self) -> str:
        """Extracts cleaned query from either 'query' or 'question' attribute."""
        return (self.query or self.question or "").strip()


class AdvisoryResult(BaseModel):
    """Farmer advisory guidance grounded in authoritative ICAR guidelines."""
    query: str = Field(..., description="Farmer query submitted")
    crop_name: Optional[str] = Field(None, description="Target crop context")
    answer: str = Field(..., description="Actionable, jargon-free advice with dosages")
    sources: List[str] = Field(default_factory=list, description="Authoritative sources (e.g. ICAR guidelines)")
    urgency_level: str = Field("Normal", description="Urgency rating: Normal, Advisory, Urgent")
    helpline: str = Field("Kisan Call Centre: 1800-180-1551", description="Free telephonic helpline")


# =============================================================================
# 3. SOIL HEALTH CARD 12-PARAMETER MODELS
# =============================================================================

class SoilReportInput(BaseModel):
    """12-parameter Soil Health Card diagnostic input with normalization."""
    crop: str = Field(..., description="Crop name (e.g. Rice, Wheat, Tomato, Sunflower)")
    target_yield: Optional[float] = Field(None, description="Target yield in tonnes/ha")
    nitrogen: float = Field(..., ge=0.0, description="Available Soil Nitrogen (N) in kg/ha")
    phosphorus: float = Field(..., ge=0.0, description="Available Soil Phosphorus (P2O5) in kg/ha")
    potassium: float = Field(..., ge=0.0, description="Available Soil Potassium (K2O) in kg/ha")
    ph: float = Field(..., ge=0.0, le=14.0, description="Soil pH value (0.0 to 14.0)")
    electrical_conductivity: float = Field(..., ge=0.0, description="Electrical Conductivity in dS/m")
    organic_carbon: float = Field(..., ge=0.0, description="Organic Carbon percentage (%)")
    area_acres: float = Field(1.0, description="Farm field size in acres (defaults safely to 1.0 if <= 0)")
    
    # Secondary and micronutrients
    sulphur: Optional[float] = Field(None, ge=0.0, description="Available Sulphur in ppm/kg/ha")
    zinc: Optional[float] = Field(None, ge=0.0, description="Available Zinc in ppm")
    boron: Optional[float] = Field(None, ge=0.0, description="Available Boron in ppm")
    iron: Optional[float] = Field(None, ge=0.0, description="Available Iron in ppm")
    manganese: Optional[float] = Field(None, ge=0.0, description="Available Manganese in ppm")
    copper: Optional[float] = Field(None, ge=0.0, description="Available Copper in ppm")

    @model_validator(mode="before")
    @classmethod
    def normalize_input(cls, data: Any) -> Any:
        """Normalizes common aliases, abbreviations, and field boundary issues."""
        if isinstance(data, dict):
            # Normalize crop / crop_name
            if "crop_name" in data and "crop" not in data:
                data["crop"] = data["crop_name"]
            # Normalize abbreviations: ec -> electrical_conductivity, oc -> organic_carbon
            if "ec" in data and "electrical_conductivity" not in data:
                data["electrical_conductivity"] = data["ec"]
            if "oc" in data and "organic_carbon" not in data:
                data["organic_carbon"] = data["oc"]
            # Normalize area units: area_hectares -> area_acres
            if "area_hectares" in data and "area_acres" not in data:
                data["area_acres"] = float(data["area_hectares"]) * 2.47105
            # Safe area clamping for non-positive values
            if "area_acres" in data and (data["area_acres"] is None or float(data["area_acres"]) <= 0):
                data["area_acres"] = 1.0
        return data


class SoilReportOutput(BaseModel):
    """Actionable commercial fertilizer recommendation and split application schedule."""
    ph_status: str = Field(..., description="Soil acidity/alkalinity diagnostic status")
    amendment_needed: Optional[str] = Field(None, description="Prescribed soil amendment (Lime or Gypsum)")
    urea_kg: float = Field(..., ge=0.0, description="Total Neem-Coated Urea in kg")
    dap_kg: float = Field(..., ge=0.0, description="Total Di-Ammonium Phosphate in kg")
    mop_kg: float = Field(..., ge=0.0, description="Total Muriate of Potash in kg")
    zinc_sulphate_kg: Optional[float] = Field(None, ge=0.0, description="Zinc Sulphate (21%) in kg")
    application_schedule: List[str] = Field(default_factory=list, description="Stage-wise fertilizer split schedule")
    
    # Extended diagnostic parameters
    ssp_kg: Optional[float] = None
    lime_kg: Optional[float] = None
    gypsum_kg: Optional[float] = None
    borax_kg: Optional[float] = None
    nitrogen_status: Optional[str] = None
    phosphorus_status: Optional[str] = None
    potassium_status: Optional[str] = None
    organic_carbon_status: Optional[str] = None
    electrical_conductivity_status: Optional[str] = None
    bags_summary: Optional[Dict[str, float]] = None


# =============================================================================
# 4. CHAT API MODELS
# =============================================================================

class ChatRequest(BaseModel):
    """Multi-turn farmer chat question submission."""
    message: Optional[str] = Field(None, description="Farmer message string")
    question: Optional[str] = Field(None, description="Alias for message")
    crop_name: Optional[str] = Field(None, description="Optional target crop context")
    language: Optional[str] = Field("en", description="Target 22 Indian language code")
    history: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Prior conversation history")

    def get_message(self) -> str:
        """Extracts cleaned message from either 'message' or 'question' attribute."""
        return (self.message or self.question or "").strip()


class ChatResponse(BaseModel):
    """Farmer chat reply with multi-turn grounding and synchronized aliases."""
    reply: str = Field(..., description="Farmer-facing advisory answer")
    response: Optional[str] = Field(None, description="Mirror of reply for client compatibility")
    sources: List[str] = Field(default_factory=lambda: ["ICAR Package of Practices"])
    urgency_level: str = "Normal"
    helpline: str = "Kisan Call Centre: 1800-180-1551"

    @model_validator(mode="after")
    def sync_response(self) -> "ChatResponse":
        """Ensure response matches reply for frontend compatibility."""
        if self.response is None:
            self.response = self.reply
        return self


# =============================================================================
# 5. SYSTEM DIAGNOSTIC MODELS
# =============================================================================

class SystemHealthResponse(BaseModel):
    """System health diagnostic response."""
    status: str = Field("ready", description="Overall health state")
    ollama_status: str = Field("ready", description="Local LLM service readiness")
    chromadb_status: str = Field("ready", description="Persistent vector store readiness")
    vision_model_status: str = Field("ready", description="Vision pipeline models readiness")
    total_documents: int = Field(..., description="Number of indexed knowledge chunks")
    server_mode: str = Field("offline", description="100% offline local execution mode")
    edge_access: Optional[str] = Field(None, description="Hotspot URL for Raspberry Pi edge client")


class SystemStatusResponse(BaseModel):
    """Comprehensive system status and hardware diagnostic response."""
    server_mode: str = "offline"
    edge_access: str
    device: str
    gpu_available: bool
    gpu_device_name: Optional[str] = None
    memory: Dict[str, Any]
    models: Dict[str, str]
    active_workers: int = 1


# =============================================================================
# 6. DYNAMIC RE-LOCALIZATION REQUEST MODELS
# =============================================================================

class LocalizeCropRequest(BaseModel):
    """Payload to dynamically re-localize a CropAnalysisResult into another language."""
    result: CropAnalysisResult
    language: str = "en"


class LocalizePestRequest(BaseModel):
    """Payload to dynamically re-localize pest detection findings into another language."""
    pest_result: Dict[str, Any]
    language: str = "en"


class LocalizeChatRequest(BaseModel):
    """Payload to dynamically re-localize conversation history into another language."""
    messages: List[Dict[str, Any]]
    language: str = "en"
