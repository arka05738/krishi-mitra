"""
Soil Health Card (SHC) 12-Parameter Diagnostic & Commercial Fertilizer Engine.
Authoritative ICAR / TNAU / DAC&FW Agronomic Standard Implementation.
Grounded in india_farmer_advisory_rag_knowledge_base.md (CHUNK-03 & CHUNK-04).
"""

from typing import List, Optional, Dict, Tuple
from pydantic import BaseModel, Field


# ==============================================================================
# 1. INTERFACE CONTRACTS (Strictly Matching PROJECT.md & SCOPE.md)
# ==============================================================================

class SoilReportInput(BaseModel):
    crop: str = Field(..., description="Crop name (e.g., 'Rice', 'Wheat', 'Tomato', 'Sunflower')")
    target_yield: Optional[float] = Field(None, description="Optional target yield in tonnes/ha")
    nitrogen: float = Field(..., ge=0.0, description="Available Soil Nitrogen in kg/ha")
    phosphorus: float = Field(..., ge=0.0, description="Available Soil Phosphorus (P2O5) in kg/ha")
    potassium: float = Field(..., ge=0.0, description="Available Soil Potassium (K2O) in kg/ha")
    ph: float = Field(..., ge=0.0, le=14.0, description="Soil pH value (0.0 to 14.0)")
    electrical_conductivity: float = Field(..., ge=0.0, description="Electrical Conductivity in dS/m")
    organic_carbon: float = Field(..., ge=0.0, description="Organic Carbon percentage (%)")
    area_acres: float = Field(1.0, gt=0.0, description="Farm field size in acres")

    # Extended optional parameters for full 12-parameter diagnostics
    sulphur: Optional[float] = Field(None, ge=0.0, description="Available Sulphur in ppm")
    zinc: Optional[float] = Field(None, ge=0.0, description="Available Zinc in ppm")
    boron: Optional[float] = Field(None, ge=0.0, description="Available Boron in ppm")
    iron: Optional[float] = Field(None, ge=0.0, description="Available Iron in ppm")
    manganese: Optional[float] = Field(None, ge=0.0, description="Available Manganese in ppm")
    copper: Optional[float] = Field(None, ge=0.0, description="Available Copper in ppm")


class SoilReportOutput(BaseModel):
    ph_status: str = Field(..., description="Classification of soil pH")
    amendment_needed: Optional[str] = Field(None, description="Recommended chemical amendment (Lime, Gypsum, or None)")
    urea_kg: float = Field(..., ge=0.0, description="Recommended Neem-Coated Urea in kg for total area")
    dap_kg: float = Field(..., ge=0.0, description="Recommended Di-Ammonium Phosphate (DAP) in kg for total area")
    mop_kg: float = Field(..., ge=0.0, description="Recommended Muriate of Potash (MOP) in kg for total area")
    zinc_sulphate_kg: Optional[float] = Field(None, ge=0.0, description="Recommended Zinc Sulphate heptahydrate (21% Zn) in kg")
    application_schedule: List[str] = Field(..., description="Stage-wise splitting instructions with exact kg dosages")

    # Rich diagnostics & commercial packaging metadata
    ssp_kg: Optional[float] = Field(None, description="Alternative Single Super Phosphate (16% P2O5) in kg")
    lime_kg: Optional[float] = Field(None, description="Agricultural Lime (CaCO3) in kg")
    gypsum_kg: Optional[float] = Field(None, description="Agricultural Gypsum (CaSO4.2H2O) in kg")
    borax_kg: Optional[float] = Field(None, description="Borax (10.5% B) in kg")
    nitrogen_status: Optional[str] = Field(None, description="Low, Medium, or High status for N")
    phosphorus_status: Optional[str] = Field(None, description="Low, Medium, or High status for P2O5")
    potassium_status: Optional[str] = Field(None, description="Low, Medium, or High status for K2O")
    organic_carbon_status: Optional[str] = Field(None, description="Low, Medium, or High status for OC")
    electrical_conductivity_status: Optional[str] = Field(None, description="Normal, Critical, or Saline status for EC")
    bags_summary: Optional[Dict[str, float]] = Field(None, description="Commercial bag equivalents (45kg Urea, 50kg DAP/SSP/MOP)")


# ==============================================================================
# 2. CROP PRODUCTION DATABASE (ICAR / TNAU Package of Practices)
# ==============================================================================

CROP_DATABASE: Dict[str, Dict] = {
    "rice": {
        "display_name": "Rice / Paddy (Kharif Aman HYV)",
        "base_rdf": {"n": 80.0, "p2o5": 40.0, "k2o": 40.0},
        "prefer_ssp": False,
        "default_zn_kg_ha": 25.0,
        "splits": [
            {"stage": "Basal at Final Puddling", "n_pct": 0.25, "p_pct": 1.00, "k_pct": 0.50, "include_zn": True},
            {"stage": "Active Tillering (21 DAT)", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00, "include_zn": False},
            {"stage": "Panicle Initiation (42–45 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.50, "include_zn": False},
        ],
    },
    "rice_boro": {
        "display_name": "Rice / Paddy (Summer Boro Irrigated HYV)",
        "base_rdf": {"n": 120.0, "p2o5": 60.0, "k2o": 60.0},
        "prefer_ssp": False,
        "default_zn_kg_ha": 25.0,
        "splits": [
            {"stage": "Basal at Puddling", "n_pct": 0.25, "p_pct": 1.00, "k_pct": 0.50, "include_zn": True},
            {"stage": "Active Tillering (21 DAT)", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00, "include_zn": False},
            {"stage": "Panicle Initiation (45 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.50, "include_zn": False},
        ],
    },
    "wheat": {
        "display_name": "Wheat (Timely Sown Irrigated)",
        "base_rdf": {"n": 120.0, "p2o5": 60.0, "k2o": 40.0},
        "prefer_ssp": False,
        "default_zn_kg_ha": 25.0,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 1.00, "include_zn": True},
            {"stage": "Crown Root Initiation - CRI (20–25 DAS)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00, "include_zn": False},
            {"stage": "Late Tillering / Jointing (40–45 DAS)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00, "include_zn": False},
        ],
    },
    "maize": {
        "display_name": "Maize / Corn (Kharif Hybrid)",
        "base_rdf": {"n": 150.0, "p2o5": 75.0, "k2o": 75.0},
        "prefer_ssp": False,
        "default_zn_kg_ha": 25.0,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 0.25, "p_pct": 1.00, "k_pct": 1.00, "include_zn": True},
            {"stage": "Knee-High Stage (25–30 DAS)", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00, "include_zn": False},
            {"stage": "Tasseling Stage (45–50 DAS)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00, "include_zn": False},
        ],
    },
    "mustard": {
        "display_name": "Rapeseed-Mustard",
        "base_rdf": {"n": 80.0, "p2o5": 40.0, "k2o": 40.0},
        "prefer_ssp": True,
        "default_s_kg_ha": 30.0,
        "default_borax_kg_ha": 10.0,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 1.00, "include_s": True, "include_b": True},
            {"stage": "Pre-Flowering / First Irrigation (30–35 DAS)", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00},
        ],
    },
    "groundnut": {
        "display_name": "Groundnut / Peanut",
        "base_rdf": {"n": 25.0, "p2o5": 50.0, "k2o": 75.0},
        "prefer_ssp": True,
        "default_gypsum_kg_ha": 400.0,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 1.00, "p_pct": 1.00, "k_pct": 1.00},
            {"stage": "Pegging Stage (40–45 DAS)", "n_pct": 0.00, "p_pct": 0.00, "k_pct": 0.00, "include_gypsum": True},
        ],
    },
    "chickpea": {
        "display_name": "Chickpea / Pulses",
        "base_rdf": {"n": 20.0, "p2o5": 40.0, "k2o": 20.0},
        "prefer_ssp": True,
        "default_s_kg_ha": 20.0,
        "splits": [
            {"stage": "Basal Starter Placement at Sowing", "n_pct": 1.00, "p_pct": 1.00, "k_pct": 1.00, "include_s": True},
        ],
    },
    "potato": {
        "display_name": "Potato",
        "base_rdf": {"n": 150.0, "p2o5": 100.0, "k2o": 100.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Basal Placement in Furrows", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 1.00},
            {"stage": "First Earthing-Up (25–30 DAP)", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00},
        ],
    },
    "cotton": {
        "display_name": "Bt-Cotton",
        "base_rdf": {"n": 150.0, "p2o5": 75.0, "k2o": 75.0},
        "prefer_ssp": False,
        "default_zn_kg_ha": 10.0,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 0.25, "p_pct": 1.00, "k_pct": 0.50, "include_zn": True},
            {"stage": "Square Initiation (35–40 DAS)", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00},
            {"stage": "Peak Flowering / Boll Formation (65–70 DAS)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.50},
        ],
    },
    "tomato": {
        "display_name": "Tomato (F1 Hybrid)",
        "base_rdf": {"n": 150.0, "p2o5": 75.0, "k2o": 75.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Basal at Transplanting", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 0.50},
            {"stage": "Vegetative Growth (30 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.25},
            {"stage": "Fruit Set (50 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.25},
        ],
    },
    "brinjal": {
        "display_name": "Brinjal / Eggplant",
        "base_rdf": {"n": 150.0, "p2o5": 75.0, "k2o": 75.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Basal at Transplanting", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 0.50},
            {"stage": "Top-Dressing 1 (30 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
            {"stage": "Top-Dressing 2 (45 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.50},
        ],
    },
    "chilli": {
        "display_name": "Chilli / Hot Pepper",
        "base_rdf": {"n": 120.0, "p2o5": 60.0, "k2o": 60.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Basal at Transplanting", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 0.50},
            {"stage": "Top-Dressing 1 (30 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
            {"stage": "Top-Dressing 2 (60 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.50},
        ],
    },
    "okra": {
        "display_name": "Okra / Bhindi",
        "base_rdf": {"n": 100.0, "p2o5": 50.0, "k2o": 50.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 1.00},
            {"stage": "Top-Dressing 1 (30 DAS)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
            {"stage": "Top-Dressing 2 (45 DAS)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
        ],
    },
    "cabbage": {
        "display_name": "Cabbage / Cauliflower",
        "base_rdf": {"n": 120.0, "p2o5": 60.0, "k2o": 60.0},
        "prefer_ssp": False,
        "default_borax_kg_ha": 10.0,
        "splits": [
            {"stage": "Basal at Transplanting", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 1.00, "include_b": True},
            {"stage": "Top-Dressing 1 (30 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
            {"stage": "Top-Dressing 2 (45 DAT)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
        ],
    },
    "cucurbits": {
        "display_name": "Cucurbits (Cucumber / Gourds)",
        "base_rdf": {"n": 100.0, "p2o5": 50.0, "k2o": 50.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 1.00},
            {"stage": "Vine Elongation (30 DAS)", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00},
        ],
    },
    "sunflower": {
        "display_name": "Sunflower",
        "base_rdf": {"n": 80.0, "p2o5": 60.0, "k2o": 40.0},
        "prefer_ssp": True,
        "default_s_kg_ha": 25.0,
        "default_borax_kg_ha": 10.0,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 1.00, "include_s": True, "include_b": True},
            {"stage": "Button Stage (30–35 DAS)", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00},
        ],
    },
    "sugarcane": {
        "display_name": "Sugarcane (Suru)",
        "base_rdf": {"n": 250.0, "p2o5": 115.0, "k2o": 115.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Planting (Basal)", "n_pct": 0.25, "p_pct": 1.00, "k_pct": 1.00},
            {"stage": "6 Weeks after Planting", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
            {"stage": "12 Weeks after Planting", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
            {"stage": "Earthing-Up (16–18 Weeks)", "n_pct": 0.25, "p_pct": 0.00, "k_pct": 0.00},
        ],
    },
    "jute": {
        "display_name": "Jute (Tossa / White)",
        "base_rdf": {"n": 60.0, "p2o5": 30.0, "k2o": 30.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Basal at Sowing", "n_pct": 0.333, "p_pct": 1.00, "k_pct": 1.00},
            {"stage": "21 DAS (Weeding)", "n_pct": 0.333, "p_pct": 0.00, "k_pct": 0.00},
            {"stage": "35–42 DAS", "n_pct": 0.334, "p_pct": 0.00, "k_pct": 0.00},
        ],
    },
    "default": {
        "display_name": "Field Crop (General Advisory)",
        "base_rdf": {"n": 100.0, "p2o5": 50.0, "k2o": 50.0},
        "prefer_ssp": False,
        "splits": [
            {"stage": "Basal at Sowing / Planting", "n_pct": 0.50, "p_pct": 1.00, "k_pct": 1.00},
            {"stage": "Active Vegetative Top-Dressing", "n_pct": 0.50, "p_pct": 0.00, "k_pct": 0.00},
        ],
    }
}


# ==============================================================================
# 3. CORE DIAGNOSTIC CLASSIFIERS
# ==============================================================================

def classify_soil_ph(ph: float, area_ha: float) -> Tuple[str, Optional[str], Optional[float], Optional[float]]:
    """
    Classifies soil pH and computes Lime or Gypsum requirements.
    Returns: (ph_status, amendment_text, lime_kg, gypsum_kg)
    """
    lime_kg = None
    gypsum_kg = None

    if ph < 5.5:
        ph_status = f"Strongly Acidic (pH {ph:.1f})"
        rate_ha = 400.0  # 400 kg/ha
        lime_kg = round(rate_ha * area_ha, 1)
        amendment_text = (
            f"Strongly Acidic Soil: Apply Agricultural Lime (CaCO3) or Dolomite @ {lime_kg} kg "
            f"for this plot ({rate_ha:.0f} kg/ha) in furrows 15 days before sowing. Avoid acid-forming fertilizers."
        )
    elif ph < 6.5:
        ph_status = f"Moderately Acidic (pH {ph:.1f})"
        rate_ha = 300.0  # 300 kg/ha
        lime_kg = round(rate_ha * area_ha, 1)
        amendment_text = (
            f"Acidic Soil: Apply Agricultural Lime (CaCO3) @ {lime_kg} kg "
            f"for this plot ({rate_ha:.0f} kg/ha) during land preparation to unlock soil phosphorus."
        )
    elif ph <= 7.5:
        ph_status = f"Neutral / Optimal (pH {ph:.1f})"
        amendment_text = None
    elif ph <= 8.5:
        ph_status = f"Moderately Alkaline (pH {ph:.1f})"
        rate_ha = 400.0
        gypsum_kg = round(rate_ha * area_ha, 1)
        amendment_text = (
            f"Alkaline Soil: Apply Agricultural Gypsum (CaSO4.2H2O) @ {gypsum_kg} kg "
            f"for this plot ({rate_ha:.0f} kg/ha) + incorporate Dhaincha green manure."
        )
    else:
        ph_status = f"Sodic / Alkali (pH {ph:.1f})"
        rate_ha = 600.0
        gypsum_kg = round(rate_ha * area_ha, 1)
        amendment_text = (
            f"Sodic / Alkali Soil: Broadcast Agricultural Gypsum @ {gypsum_kg} kg "
            f"for this plot ({rate_ha:.0f} kg/ha), incorporate into plough depth, and leach with fresh water."
        )

    return ph_status, amendment_text, lime_kg, gypsum_kg


def classify_ec(ec: float) -> str:
    if ec < 1.0:
        return "Normal / Non-saline (< 1.0 dS/m)"
    elif ec <= 2.0:
        return "Critical Range (1.0–2.0 dS/m) - Salt-sensitive crops require good drainage"
    else:
        return f"Saline Hazard ({ec:.1f} dS/m > 2.0) - Root zone leaching & salt-tolerant cultivars required"


def classify_oc(oc: float) -> str:
    if oc < 0.50:
        return f"Low ({oc:.2f}% < 0.50%) - Apply FYM @ 10–15 t/ha or Vermicompost @ 2.5–5 t/ha"
    elif oc <= 0.75:
        return f"Medium ({oc:.2f}%) - Maintain with 5–8 t/ha organic manure"
    else:
        return f"High ({oc:.2f}% > 0.75%) - Optimal soil organic carbon pool"


def classify_primary_nutrient(value: float, nutrient: str) -> Tuple[str, float]:
    """
    Classifies N, P, or K into Low (+25%), Medium (0%), High (-25%).
    Returns: (rating_category, stcr_adjustment_factor)
    """
    n_lower = nutrient.lower()
    if n_lower == "n":
        if value < 280.0:
            return "Low (< 280 kg/ha)", 1.25
        elif value <= 560.0:
            return "Medium (280–560 kg/ha)", 1.00
        else:
            return "High (> 560 kg/ha)", 0.75
    elif n_lower in ("p", "p2o5"):
        if value < 23.0:
            return "Low (< 23 kg P2O5/ha)", 1.25
        elif value <= 57.0:
            return "Medium (23–57 kg P2O5/ha)", 1.00
        else:
            return "High (> 57 kg P2O5/ha)", 0.75
    elif n_lower in ("k", "k2o"):
        if value < 120.0:
            return "Low (< 120 kg K2O/ha)", 1.25
        elif value <= 280.0:
            return "Medium (120–280 kg K2O/ha)", 1.00
        else:
            return "High (> 280 kg K2O/ha)", 0.75
    else:
        return "Medium", 1.00


def get_crop_profile(crop_input: str = "", crop_name: Optional[str] = None) -> Dict:
    """Finds matching crop profile from CROP_DATABASE using fuzzy token matching."""
    actual_crop = crop_name if crop_name is not None else crop_input
    if not actual_crop or not actual_crop.strip():
        return CROP_DATABASE["default"]

    crop_clean = actual_crop.strip().lower()
    for key, profile in CROP_DATABASE.items():
        if key == "default":
            continue
        if crop_clean and (crop_clean in key or key in crop_clean):
            return profile
    # Common synonyms and vernacular names
    if "paddy" in crop_clean or "dhan" in crop_clean or "swarna" in crop_clean or "aman" in crop_clean:
        return CROP_DATABASE["rice"]
    if "boro" in crop_clean:
        return CROP_DATABASE["rice_boro"]
    if "corn" in crop_clean or "makka" in crop_clean:
        return CROP_DATABASE["maize"]
    if "sarson" in crop_clean or "toria" in crop_clean or "rai" in crop_clean:
        return CROP_DATABASE["mustard"]
    if "peanut" in crop_clean or "moongphali" in crop_clean:
        return CROP_DATABASE["groundnut"]
    if "chana" in crop_clean or "gram" in crop_clean or "pulse" in crop_clean:
        return CROP_DATABASE["chickpea"]
    if "alu" in crop_clean or "aloo" in crop_clean:
        return CROP_DATABASE["potato"]
    if "surajmukhi" in crop_clean:
        return CROP_DATABASE["sunflower"]
    if "baingan" in crop_clean or "eggplant" in crop_clean:
        return CROP_DATABASE["brinjal"]
    if "mirch" in crop_clean or "pepper" in crop_clean:
        return CROP_DATABASE["chilli"]
    if "bhindi" in crop_clean:
        return CROP_DATABASE["okra"]
    if "gobhi" in crop_clean or "cauliflower" in crop_clean:
        return CROP_DATABASE["cabbage"]
    if "kheera" in crop_clean or "cucumber" in crop_clean or "gourd" in crop_clean:
        return CROP_DATABASE["cucurbits"]
    if "ganna" in crop_clean:
        return CROP_DATABASE["sugarcane"]
    if "pat" in crop_clean:
        return CROP_DATABASE["jute"]
    return CROP_DATABASE["default"]


# ==============================================================================
# 4. MAIN AGRO-CALCULATOR ENGINE
# ==============================================================================

def calculate_soil_health(report: SoilReportInput) -> SoilReportOutput:
    """
    Executes the 12-parameter agronomic diagnostic and commercial fertilizer calculation.
    """
    area_acres = max(0.01, report.area_acres)
    area_ha = area_acres * 0.404686  # 1 acre = 0.404686 ha

    # 1. Physical & Biological Diagnostics
    ph_status, amendment_text, lime_kg, gypsum_kg = classify_soil_ph(report.ph, area_ha)
    ec_status = classify_ec(report.electrical_conductivity)
    oc_status = classify_oc(report.organic_carbon)

    # 2. Crop Profile & Base RDF
    crop_info = get_crop_profile(report.crop)
    base_n = crop_info["base_rdf"]["n"]
    base_p = crop_info["base_rdf"]["p2o5"]
    base_k = crop_info["base_rdf"]["k2o"]

    # 3. STCR Primary Nutrient Adjustments
    n_status, n_factor = classify_primary_nutrient(report.nitrogen, "n")
    p_status, p_factor = classify_primary_nutrient(report.phosphorus, "p2o5")
    k_status, k_factor = classify_primary_nutrient(report.potassium, "k2o")

    adj_n_ha = base_n * n_factor
    adj_p_ha = base_p * p_factor
    adj_k_ha = base_k * k_factor

    # 4. Fertilizer Calculations for Farm Area (Combination B: DAP + Urea + MOP)
    field_n = adj_n_ha * area_ha
    field_p = adj_p_ha * area_ha
    field_k = adj_k_ha * area_ha

    # DAP supplies 46% P2O5 and 18% N
    dap_kg = field_p / 0.46
    n_from_dap = dap_kg * 0.18

    # MANDATORY DAP-N deduction: remaining N supplied by Urea (46% N)
    remaining_n = max(0.0, field_n - n_from_dap)
    urea_kg = remaining_n / 0.46

    # MOP supplies 60% K2O
    mop_kg = field_k / 0.60

    # Combination A alternative (SSP supplies 16% P2O5, 11% S)
    ssp_kg = field_p / 0.16

    # 5. Micronutrient Diagnostics & Calculations
    zinc_kg = None
    if report.zinc is not None and report.zinc < 0.6:
        zinc_kg = round(25.0 * area_ha, 1)
    elif crop_info.get("default_zn_kg_ha"):
        zinc_kg = round(crop_info["default_zn_kg_ha"] * area_ha, 1)

    borax_kg = None
    if report.boron is not None and report.boron < 0.5:
        borax_kg = round(10.0 * area_ha, 1)
    elif crop_info.get("default_borax_kg_ha"):
        borax_kg = round(crop_info["default_borax_kg_ha"] * area_ha, 1)

    if crop_info.get("default_gypsum_kg_ha") and gypsum_kg is None:
        gypsum_kg = round(crop_info["default_gypsum_kg_ha"] * area_ha, 1)
        if amendment_text is None:
            amendment_text = f"Crop Requirement: Apply Gypsum @ {gypsum_kg} kg at pegging stage."

    # 6. Commercial Bag Summary
    bags = {
        "urea_bags_45kg": round(urea_kg / 45.0, 1),
        "dap_bags_50kg": round(dap_kg / 50.0, 1),
        "mop_bags_50kg": round(mop_kg / 50.0, 1),
        "ssp_bags_50kg": round(ssp_kg / 50.0, 1),
    }

    # 7. Generate Actionable Application Schedule
    schedule: List[str] = []
    splits = crop_info.get("splits", [])

    for split in splits:
        stage_title = split["stage"]
        stage_n_kg = round(urea_kg * split.get("n_pct", 0.0), 1)
        stage_p_kg = round(dap_kg * split.get("p_pct", 0.0), 1)
        stage_k_kg = round(mop_kg * split.get("k_pct", 0.0), 1)

        items = []
        if stage_p_kg > 0:
            items.append(f"DAP: {stage_p_kg} kg")
        if stage_n_kg > 0:
            items.append(f"Neem-Coated Urea: {stage_n_kg} kg")
        if stage_k_kg > 0:
            items.append(f"MOP: {stage_k_kg} kg")
        if split.get("include_zn") and zinc_kg:
            items.append(f"Zinc Sulphate (21%): {zinc_kg} kg (apply separately with sand/FYM)")
        if split.get("include_gypsum") and gypsum_kg:
            items.append(f"Agricultural Gypsum: {gypsum_kg} kg")
        if split.get("include_b") and borax_kg:
            items.append(f"Borax (10.5% B): {borax_kg} kg")

        if items:
            schedule.append(f"[{stage_title}] Apply: " + ", ".join(items))

    # Add agronomic cautions to schedule
    if zinc_kg and dap_kg > 0:
        schedule.append(
            "[Important Guardrail] Never mix Zinc Sulphate directly with DAP or SSP in the same container. "
            "Mix Zinc Sulphate with dry soil/sand or well-rotted FYM and broadcast separately."
        )

    return SoilReportOutput(
        ph_status=ph_status,
        amendment_needed=amendment_text,
        urea_kg=round(urea_kg, 1),
        dap_kg=round(dap_kg, 1),
        mop_kg=round(mop_kg, 1),
        zinc_sulphate_kg=zinc_kg,
        application_schedule=schedule,
        ssp_kg=round(ssp_kg, 1),
        lime_kg=lime_kg,
        gypsum_kg=gypsum_kg,
        borax_kg=borax_kg,
        nitrogen_status=n_status,
        phosphorus_status=p_status,
        potassium_status=k_status,
        organic_carbon_status=oc_status,
        electrical_conductivity_status=ec_status,
        bags_summary=bags,
    )


def calculate_fertilizer_recommendation(report: SoilReportInput) -> SoilReportOutput:
    """Alias for calculate_soil_health for API backwards compatibility."""
    return calculate_soil_health(report)
