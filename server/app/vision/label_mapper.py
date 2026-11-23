# Label and Quality Grade Mapper for Offline Crop Leaf Analysis
"""
Farmer-friendly translation and quality grading engine.
Translates technical vision model outputs into clean, respectful, jargon-free agricultural advice.
"""

import math
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field


class CropAnalysisResult(BaseModel):
    """Structured crop analysis result matching project interface contract."""
    crop_name: str = Field(..., description="Clean name of crop or flower, e.g. Tomato, Sunflower")
    detected_condition: str = Field(..., description="Condition name in farmer terminology")
    quality_grade: str = Field(..., description="Grade A (Prime), Grade B (Early Attention), Grade C (Health Risk)")
    quality_score: int = Field(..., ge=0, le=100, description="Quality percentage score from 0 to 100")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Model classification confidence from 0.0 to 1.0")
    severity: str = Field(..., description="Severity level: None, Mild, Moderate, or Critical")
    summary: str = Field(..., description="Respectful, plain-language explanation with zero technical jargon")
    recommended_action: List[str] = Field(..., min_length=1, description="Practical, agricultural remedial actions")
    is_crop: bool = Field(default=True, description="Whether image contains an agricultural crop, leaf, or flower")
    raw_label: Optional[str] = Field(default=None, description="Original raw label key for lossless localization")


# Comprehensive mapping metadata for all 38 PlantVillage classes + Sunflower classes
LABEL_DATABASE: Dict[str, Dict[str, Any]] = {
    # ------------------ APPLE ------------------
    "Apple___Apple_scab": {
        "crop_name": "Apple",
        "detected_condition": "Apple Scab (Olive-Black Velvety Spots)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Mild",
        "base_score": 68,
        "summary": (
            "The foliage displays dark, olive-green velvety lesions characteristic of apple scab. "
            "Timely treatment preserves active leaves and protects future fruit quality."
        ),
        "recommended_action": [
            "Apply bio-fungicide (Trichoderma viride or Bacillus subtilis) or protective copper spray.",
            "Prune inner branches to improve sun exposure and rapid leaf drying after rain.",
            "Rake and safely compost or burn fallen leaves to reduce overwintering fungal spores.",
            "Avoid overhead sprinkler watering on the tree canopy."
        ]
    },
    "Apple___Black_rot": {
        "crop_name": "Apple",
        "detected_condition": "Black Rot (Frogeye Leaf Spot)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 35,
        "summary": (
            "Dark brown circular spots with purple margins and dead tissue indicate black rot fungal infection. "
            "This condition requires prompt orchard sanitation to prevent spread to fruit and branches."
        ),
        "recommended_action": [
            "Prune out dead wood, cankered twigs, and mummified fruits hanging on branches.",
            "Apply copper oxychloride (3 g/L) or protective fungicide during clear weather.",
            "Disinfect pruning shears with clean spirit or bleach solution between trees.",
            "Maintain balanced tree nutrition with organic compost and potash."
        ]
    },
    "Apple___Cedar_apple_rust": {
        "crop_name": "Apple",
        "detected_condition": "Cedar Apple Rust (Bright Orange Spots)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 62,
        "summary": (
            "Bright orange-yellow spots on the upper leaf surface indicate cedar apple rust. "
            "This fungus moves between apple trees and nearby cedar or juniper trees during wet spring weather."
        ),
        "recommended_action": [
            "Clear or trim wild cedar or juniper trees within 300 meters of the orchard if feasible.",
            "Spray protective mancozeb (2.5 g/L) or neem seed kernel extract (5%) at petal drop.",
            "Rake away fallen diseased leaves to keep the orchard floor clean.",
            "Ensure good tree spacing for sunlight penetration and airflow."
        ]
    },
    "Apple___healthy": {
        "crop_name": "Apple",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 96,
        "summary": (
            "Apple leaves show strong photosynthetic vigor with deep green coloring and zero symptoms "
            "of foliar fungal pathogens or insect damage."
        ),
        "recommended_action": [
            "Maintain scheduled tree nutrition with well-rotted farmyard manure.",
            "Ensure regular orchard basin irrigation during active fruit development.",
            "Monitor tree canopy weekly for early seasonal insect pests or leaf curling.",
            "Keep orchard basin mulched to conserve moisture and suppress weeds."
        ]
    },

    # ------------------ BLUEBERRY ------------------
    "Blueberry___healthy": {
        "crop_name": "Blueberry",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 96,
        "summary": (
            "Blueberry foliage exhibits lush green color, firm leaf texture, and healthy growth "
            "without fungal spots or nutrient deficiencies."
        ),
        "recommended_action": [
            "Maintain acidic soil conditions (pH 4.5 to 5.2) using pine bark mulch or organic compost.",
            "Provide consistent moisture through drip irrigation without causing waterlogging.",
            "Apply organic nitrogen in light split doses as per crop growth stage.",
            "Scout weekly for leafhoppers or root grubs."
        ]
    },

    # ------------------ CHERRY ------------------
    "Cherry_(including_sour)___Powdery_mildew": {
        "crop_name": "Cherry",
        "detected_condition": "Powdery Mildew (White Powdery Coating)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 60,
        "summary": (
            "White powdery fungal patches are visible on leaf surfaces, causing leaf curling "
            "and reducing natural sunlight absorption."
        ),
        "recommended_action": [
            "Spray wettable sulfur (2 g/L) or potassium bicarbonate at the earliest onset.",
            "Prune congested shoots to encourage continuous air movement and sun exposure.",
            "Avoid high doses of chemical nitrogen that produce soft, vulnerable leaf growth.",
            "Apply neem oil extract (1500 ppm) during early morning or evening hours."
        ]
    },
    "Cherry_(including_sour)___healthy": {
        "crop_name": "Cherry",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 95,
        "summary": (
            "Cherry leaves are vibrant, uniformly green, and free from fungal mildew, bacterial cankers, "
            "or physical leaf scorch."
        ),
        "recommended_action": [
            "Apply balanced potassium and micronutrient spray to strengthen foliage and fruit buds.",
            "Maintain deep root irrigation during fruit sizing and dry summer spells.",
            "Inspect underside of leaves periodically for spider mites or aphids.",
            "Clean and prune branches only during dry weather to prevent bacterial infections."
        ]
    },

    # ------------------ CORN (MAIZE) ------------------
    "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot": {
        "crop_name": "Corn (Maize)",
        "detected_condition": "Gray Leaf Spot (Cercospora Lesions)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 62,
        "summary": (
            "Rectangular, tan-to-gray lesions running parallel with leaf veins indicate gray leaf spot, "
            "which reduces photosynthetic leaf area if untreated."
        ),
        "recommended_action": [
            "Apply bio-control Pseudomonas fluorescens or protective foliar fungicide (azoxystrobin).",
            "Rotate following season with non-grass crops such as chickpea, soybean, or groundnut.",
            "Practice deep plowing post-harvest to incorporate crop residue into the soil.",
            "Maintain optimal plant spacing to allow leaf canopies to dry quickly after dew."
        ]
    },
    "Corn_(maize)___Common_rust_": {
        "crop_name": "Corn (Maize)",
        "detected_condition": "Common Rust (Cinnamon-Brown Pustules)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Mild",
        "base_score": 70,
        "summary": (
            "Cinnamon-brown powdery pustules scattered across both leaf surfaces indicate common rust. "
            "Prompt field care will keep upper leaves clean during grain filling."
        ),
        "recommended_action": [
            "Spray foliar mancozeb (2.5 g/L) or neem seed kernel extract (5%) on lower leaves.",
            "Apply balanced nitrogen-potassium fertilizer to improve leaf cell wall toughness.",
            "Ensure good field drainage and avoid dense plant crowding.",
            "Remove and destroy severely affected lower leaves if small farm scale allows."
        ]
    },
    "Corn_(maize)___Northern_Leaf_Blight": {
        "crop_name": "Corn (Maize)",
        "detected_condition": "Northern Corn Leaf Blight (Cigar-Shaped Lesions)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 40,
        "summary": (
            "Large, elongated cigar-shaped grayish-green to tan lesions on foliage indicate northern leaf blight, "
            "which can burn extensive leaf area during cool, humid weather."
        ),
        "recommended_action": [
            "Apply protective mancozeb or propiconazole spray immediately to arrest fungal expansion.",
            "Deep plow or compost crop residue after harvest to break the disease cycle.",
            "Rotate the field with legumes (soybean or moong) in the upcoming season.",
            "Select certified blight-resistant hybrid varieties for future sowings."
        ]
    },
    "Corn_(maize)___healthy": {
        "crop_name": "Corn (Maize)",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 96,
        "summary": (
            "Maize foliage is deep green, broad, and free from foliar pustules or blights, "
            "supporting full photosynthetic grain production."
        ),
        "recommended_action": [
            "Apply scheduled top-dressing of urea at knee-high and tasseling stages.",
            "Maintain optimal soil moisture during critical silking and grain formation periods.",
            "Scout leaf whorls weekly for early fall armyworm caterpillars.",
            "Keep field borders clear of wild weeds."
        ]
    },

    # ------------------ GRAPE ------------------
    "Grape___Black_rot": {
        "crop_name": "Grape",
        "detected_condition": "Black Rot (Leaf Spot & Berry Rot)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 38,
        "summary": (
            "Reddish-brown circular spots with dark borders and tiny fungal specks indicate black rot, "
            "which threatens both foliage and grape bunches."
        ),
        "recommended_action": [
            "Spray copper oxychloride (2.5 g/L) or mancozeb at 10 to 14 day intervals.",
            "Prune out infected canes and remove shriveled black mummified berries from vines.",
            "Maintain open canopy trellising for rapid leaf drying after morning dew.",
            "Clear and burn dry leaves and vineyard floor debris."
        ]
    },
    "Grape___Esca_(Black_Measles)": {
        "crop_name": "Grape",
        "detected_condition": "Esca (Black Measles / Vine Decline)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 30,
        "summary": (
            "Tiger-stripe interveinal discoloration and drying on leaves indicate esca wood decline, "
            "affecting the vine vascular water transport system."
        ),
        "recommended_action": [
            "Identify and mark affected vines to avoid spreading spores during routine pruning.",
            "Disinfect pruning shears with alcohol or antiseptic between vine cuts.",
            "Seal major trunk and cane cuts with protective wound healing paste.",
            "Avoid heavy pruning during humid or drizzling weather."
        ]
    },
    "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)": {
        "crop_name": "Grape",
        "detected_condition": "Leaf Blight (Isariopsis Leaf Spot)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 58,
        "summary": (
            "Irregular brown spots with defined borders are visible on leaves, which can cause "
            "premature leaf drop if left unchecked."
        ),
        "recommended_action": [
            "Spray Bordeaux mixture (1%) or copper hydroxide on both leaf surfaces.",
            "Collect and destroy fallen infected leaves from the vineyard ground.",
            "Thin out crowded shoots to ensure proper sunlight penetration.",
            "Apply balanced muriate of potash (MOP) to boost leaf resilience."
        ]
    },
    "Grape___healthy": {
        "crop_name": "Grape",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 96,
        "summary": (
            "Grape leaves show uniform vibrant green color, strong petioles, and zero signs of mildew, "
            "black rot, or insect feeding."
        ),
        "recommended_action": [
            "Maintain proper canopy shoot positioning and shoot tipping.",
            "Follow scheduled drip fertigation with potassium and zinc.",
            "Inspect shoot tips and fruit clusters for early thrips or mealybugs.",
            "Keep the vine floor mulched with dry straw."
        ]
    },

    # ------------------ ORANGE (CITRUS) ------------------
    "Orange___Haunglongbing_(Citrus_greening)": {
        "crop_name": "Orange (Citrus)",
        "detected_condition": "Citrus Greening (Huanglongbing)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 20,
        "summary": (
            "Asymmetrical yellow blotchy mottling on leaves and yellowing veins indicate citrus greening, "
            "a serious condition spread by the citrus psyllid insect."
        ),
        "recommended_action": [
            "Control citrus psyllid insect vectors immediately using neem oil or recommended bio-sprays.",
            "Prune and safely burn dead branches; rogue out dying, non-productive trees.",
            "Apply balanced foliar micronutrient blend (Zinc, Manganese, Iron) to support surviving foliage.",
            "Source only certified disease-free grafted saplings for new plantings."
        ]
    },

    # ------------------ PEACH ------------------
    "Peach___Bacterial_spot": {
        "crop_name": "Peach",
        "detected_condition": "Bacterial Spot (Shot-Hole Lesions)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 55,
        "summary": (
            "Small water-soaked spots that turn dark and drop out leaving a shot-hole appearance on leaves "
            "indicate bacterial spot infection."
        ),
        "recommended_action": [
            "Apply copper-based protective spray at dormant stage and early fruit set.",
            "Avoid excess nitrogen fertilizer that triggers soft, highly susceptible leaf growth.",
            "Prune tree canopy to maximize interior air circulation and rapid drying.",
            "Plant windbreaks around orchard perimeter to reduce sand and wind abrasion."
        ]
    },
    "Peach___healthy": {
        "crop_name": "Peach",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 95,
        "summary": (
            "Peach foliage shows smooth green blades, clean margins, and no symptoms of bacterial spot, "
            "leaf curl, or aphid curling."
        ),
        "recommended_action": [
            "Apply organic compost and mulch around the tree root basin.",
            "Provide regular deep irrigation during fruit swelling.",
            "Inspect branch forks for peach borer gumming or scale insects.",
            "Maintain winter sanitation and remove old mummified fruits."
        ]
    },

    # ------------------ BELL PEPPER ------------------
    "Pepper,_bell___Bacterial_spot": {
        "crop_name": "Bell Pepper (Capsicum)",
        "detected_condition": "Bacterial Spot (Foliar Lesions)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 58,
        "summary": (
            "Small water-soaked, dark brown circular spots with pale margins on bell pepper leaves "
            "indicate bacterial spot infection."
        ),
        "recommended_action": [
            "Spray copper hydroxide combined with mancozeb (2 g/L) on leaves and stems.",
            "Avoid overhead sprinkler or furrow splash that wets foliage.",
            "Remove lower diseased leaves that come in direct contact with wet soil.",
            "Disinfect field stakes and harvesting crates with clean water and bleach."
        ]
    },
    "Pepper,_bell___healthy": {
        "crop_name": "Bell Pepper (Capsicum)",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 96,
        "summary": (
            "Bell pepper foliage is dark green, robust, and shows clean veins with zero signs "
            "of bacterial spot, anthracnose, or viral leaf curl."
        ),
        "recommended_action": [
            "Provide consistent soil moisture through drip lines to prevent blossom end rot.",
            "Support heavy fruiting plants with bamboo stakes or twine.",
            "Apply light dose of calcium nitrate and boron at flowering.",
            "Scout weekly for thrips or mites on tender top leaves."
        ]
    },

    # ------------------ POTATO ------------------
    "Potato___Early_blight": {
        "crop_name": "Potato",
        "detected_condition": "Early Blight (Concentric Ring Spots)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 64,
        "summary": (
            "Dark brown circular spots with concentric target-board rings on older leaves indicate early blight. "
            "Timely treatment protects the active canopy and sustains tuber enlargement."
        ),
        "recommended_action": [
            "Recommended Fungicide & Dose: Spray Mancozeb 75% WP (Indofil M-45) @ 2.5 g/L (500 g/acre) OR Copper Oxychloride 50% WP (Blitox) @ 3.0 g/L OR Azoxystrobin 23% SC @ 1.0 ml/L.",
            "Application Timing & Method: Spray in late afternoon (4:00-6:00 PM) using 150-200 L water/acre mixed with sticker (0.5 ml/L); repeat after 10-12 days if spots persist.",
            "Organic Bio-Control: Spray Trichoderma viride @ 5 g/L and prune off soil-touching lower leaves (up to 30 cm) to stop upward spore splash.",
            "Field Management: Irrigate via furrow or drip rather than overhead sprinklers; apply balanced potash (MOP) to enhance foliar resistance (PHI: 7 days)."
        ]
    },
    "Potato___Late_blight": {
        "crop_name": "Potato",
        "detected_condition": "Late Blight (Water-Soaked Dark Rot)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 25,
        "summary": (
            "Dark water-soaked irregular patches that rapidly rot and produce white fungal fuzz underneath "
            "indicate late blight, a destructive condition requiring emergency intervention."
        ),
        "recommended_action": [
            "Emergency Systemic Fungicide: Spray Cymoxanil 8% + Mancozeb 64% WP (Curzate M8) @ 2.5 g/L OR Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold) @ 2.5 g/L (500 g per acre) immediately.",
            "Application Timing & Method: Spray after morning fog/dew clears (9:00-11:00 AM) or in late afternoon (3:00-5:00 PM) using 150-200 L water/acre with sticker (0.5 ml/L). Rotate with Dimethomorph 50% WP @ 1 g/L after 7-10 days.",
            "Tuber & Field Protection: Earth up ridges high with soil to prevent fungal spores from washing down to tubers; prune and safely bury heavily infected haulms.",
            "Drainage & Nutrition: Ensure furrow drainage is clear to prevent water stagnation; stop urea application during overcast/humid periods (PHI: 7 days)."
        ]
    },
    "Potato___healthy": {
        "crop_name": "Potato",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 97,
        "summary": (
            "Potato plant leaves are vibrant green, crisp, and completely free from blight lesions, "
            "mosaic mottling, or aphid clusters."
        ),
        "recommended_action": [
            "Earth up soil around plant roots to encourage rapid tuber expansion.",
            "Maintain uniform light furrow or drip irrigation without waterlogging.",
            "Scout canopy closely during cool, overcast, and humid weather spells.",
            "Apply neem cake to the soil to prevent soil-borne pests."
        ]
    },

    # ------------------ RASPBERRY ------------------
    "Raspberry___healthy": {
        "crop_name": "Raspberry",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 95,
        "summary": (
            "Raspberry foliage shows healthy compound leaves, uniform deep green coloring, "
            "and strong cane vigor with no rust or leaf spot."
        ),
        "recommended_action": [
            "Trellis canes upright to provide full sunlight penetration and air movement.",
            "Mulch plant rows with organic compost to conserve root moisture.",
            "Provide regular drip irrigation during berry sizing.",
            "Prune out two-year-old spent canes after harvest."
        ]
    },

    # ------------------ SOYBEAN ------------------
    "Soybean___healthy": {
        "crop_name": "Soybean",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 96,
        "summary": (
            "Soybean trifoliate leaves are healthy, deep green, and free from rust pustules, "
            "yellow mosaic virus, or defoliating caterpillars."
        ),
        "recommended_action": [
            "Keep the field weed-free during the initial 30 to 40 days after sowing.",
            "Monitor root nodules to ensure effective natural nitrogen fixation.",
            "Scout for early signs of stem fly or defoliators like semiloopers.",
            "Ensure field drainage channels are clear to prevent water stagnation in heavy soils."
        ]
    },

    # ------------------ SQUASH ------------------
    "Squash___Powdery_mildew": {
        "crop_name": "Squash / Cucurbit",
        "detected_condition": "Powdery Mildew (White Talcum Growth)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 60,
        "summary": (
            "White powdery fungal coating on upper leaf surfaces and stems reduces sunlight absorption "
            "and accelerates early leaf drying."
        ),
        "recommended_action": [
            "Spray wettable sulfur (2 g/L) or potassium bicarbonate on both leaf surfaces.",
            "Apply neem oil (5 ml/L) mixed with mild organic soap water.",
            "Remove heavily infected older leaves to open up airflow through the vine.",
            "Irrigate at the vine base rather than wetting leaves with overhead water."
        ]
    },

    # ------------------ STRAWBERRY ------------------
    "Strawberry___Leaf_scorch": {
        "crop_name": "Strawberry",
        "detected_condition": "Leaf Scorch (Purple-Rimmed Spots)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Mild",
        "base_score": 68,
        "summary": (
            "Small purplish spots with dark borders that dry into scorched leaf edges indicate leaf scorch fungus. "
            "Prompt leaf sanitation keeps the crown productive."
        ),
        "recommended_action": [
            "Remove and discard scorched outer leaves during routine bed weeding.",
            "Avoid overhead watering so that the strawberry foliage stays dry.",
            "Apply protective copper-based spray after harvest to protect new leaf crowns.",
            "Renew strawberry bed mulch with clean, dry straw."
        ]
    },
    "Strawberry___healthy": {
        "crop_name": "Strawberry",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 97,
        "summary": (
            "Strawberry plant leaves are rich green, sturdy, and free from leaf spots, scorch, "
            "gray mold, or crown rot symptoms."
        ),
        "recommended_action": [
            "Keep clean dry straw mulch under runners to keep leaves and fruit off damp soil.",
            "Ensure balanced boron and potassium nutrition for fruit firmness and sweetness.",
            "Drip irrigate at the plant root zone without wetting the crowns.",
            "Monitor underleaf surfaces weekly for two-spotted spider mites."
        ]
    },

    # ------------------ TOMATO ------------------
    "Tomato___Bacterial_spot": {
        "crop_name": "Tomato",
        "detected_condition": "Bacterial Spot (Small Water-Soaked Spots)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 56,
        "summary": (
            "Small, dark brown water-soaked lesions with yellow halos on leaves indicate bacterial spot, "
            "which spreads rapidly during rainy and humid weather."
        ),
        "recommended_action": [
            "Spray copper oxychloride (2.5 g/L) combined with streptomycin sulphate on leaves.",
            "Avoid handling plants or working in the field while foliage is damp.",
            "Stake tomato vines securely to lift branches above wet ground.",
            "Collect and destroy severely spotted lower leaves to prevent splash spread."
        ]
    },
    "Tomato___Early_blight": {
        "crop_name": "Tomato",
        "detected_condition": "Early Blight (Target-Board Ring Spots)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 65,
        "summary": (
            "Dark brown concentric rings resembling a target board on lower leaves indicate early blight. "
            "Prompt removal of affected lower leaves protects productive flowering branches."
        ),
        "recommended_action": [
            "Recommended Fungicide & Dose: Spray Mancozeb 75% WP (Indofil M-45) @ 2.5 g/L (500 g/acre) OR Copper Oxychloride 50% WP (Blitox) @ 3.0 g/L OR Azoxystrobin 23% SC @ 1.0 ml/L.",
            "Application Timing & Method: Spray in late afternoon (4:00-6:00 PM) using 150-200 L water/acre mixed with sticker (0.5 ml/L); repeat after 10-12 days if spots persist.",
            "Organic Bio-Control: Spray Trichoderma viride or Pseudomonas fluorescens @ 5 g/L and prune off soil-touching lower leaves (up to 30 cm) to stop upward spore splash.",
            "Field Management: Apply straw or leaf mulch around tomato bases to prevent rain splash from soil; ensure 60 cm spacing for ventilation (PHI: 7 days)."
        ]
    },
    "Tomato___Late_blight": {
        "crop_name": "Tomato",
        "detected_condition": "Late Blight (Water-Soaked Dark Rot)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 22,
        "summary": (
            "Large water-soaked brownish-black greasy patches with delicate white fungal mold under leaves "
            "indicate late blight, an urgent condition that can rapidly collapse tomato vines."
        ),
        "recommended_action": [
            "Emergency Systemic Fungicide: Spray Cymoxanil 8% + Mancozeb 64% WP (Curzate M8) @ 2.5 g/L OR Metalaxyl 8% + Mancozeb 64% WP (Ridomil Gold) @ 2.5 g/L (500 g per acre) immediately.",
            "Application Timing & Method: Mix with agricultural sticker (0.5 ml/L) in 150-200 L water/acre; thoroughly coat upper and lower leaf surfaces during morning (9:00-11:00 AM) or late afternoon (3:00-5:00 PM). Rotate with Dimethomorph 50% WP @ 1.0 g/L after 7-10 days.",
            "Sanitation & Protection: Prune and safely bury or burn severely blighted stems away from the field to stop active fungal sporulation.",
            "Water & Soil Management: Open drainage furrows immediately to eliminate standing water; switch to furrow or drip irrigation and suspend urea top-dressing during humid overcast weather (PHI: 7 days)."
        ]
    },
    "Tomato___Leaf_Mold": {
        "crop_name": "Tomato",
        "detected_condition": "Leaf Mold (Yellow Blotches & Olive Mold)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Mild",
        "base_score": 70,
        "summary": (
            "Pale green to yellow blotches on the upper leaf surface with velvety olive-brown fungal growth "
            "underneath indicate leaf mold, common in humid enclosed spaces."
        ),
        "recommended_action": [
            "Increase side ventilation in polyhouses or prune dense leaf canopy for better airflow.",
            "Spray copper-based protective fungicide or potassium bicarbonate.",
            "Water crops early in the morning so foliage dries quickly during the day.",
            "Remove heavily colonized bottom leaves."
        ]
    },
    "Tomato___Septoria_leaf_spot": {
        "crop_name": "Tomato",
        "detected_condition": "Septoria Leaf Spot (Small Circular Spots)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 62,
        "summary": (
            "Numerous small circular brown spots with light gray centers and dark borders on lower leaves "
            "indicate septoria leaf spot, which progresses from bottom to top."
        ),
        "recommended_action": [
            "Prune off affected lower leaves showing heavy gray spotting.",
            "Apply protective chlorothalonil or mancozeb spray covering both leaf sides.",
            "Apply organic mulch around the stem base to block soil spore splash.",
            "Rotate the plot away from solanaceous crops in the next planting cycle."
        ]
    },
    "Tomato___Spider_mites Two-spotted_spider_mite": {
        "crop_name": "Tomato",
        "detected_condition": "Two-Spotted Spider Mites (Foliar Stippling & Webbing)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 60,
        "summary": (
            "Fine yellow stippling on leaf blades accompanied by delicate silk webbing underneath "
            "indicates spider mite activity, typically during hot dry spells."
        ),
        "recommended_action": [
            "Spray neem oil (1500 ppm) or botanical insecticidal soap targeting the leaf undersides.",
            "Apply wettable sulfur spray during cooler evening hours.",
            "Sprinkle water on field pathways to raise humidity and suppress mite buildup.",
            "Remove and destroy severely webbed shoots."
        ]
    },
    "Tomato___Target_Spot": {
        "crop_name": "Tomato",
        "detected_condition": "Target Spot (Corynespora Leaf Lesions)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Moderate",
        "base_score": 60,
        "summary": (
            "Brown circular lesions with prominent concentric rings and yellow margins indicate target spot "
            "fungal infection on foliage."
        ),
        "recommended_action": [
            "Spray azoxystrobin or copper-based fungicide at the first sign of lesions.",
            "Stake and prune tomato vines to promote rapid leaf drying.",
            "Remove crop debris after harvest to prevent spores from carrying over.",
            "Maintain balanced nitrogen and potassium fertilization."
        ]
    },
    "Tomato___Tomato_Yellow_Leaf_Curl_Virus": {
        "crop_name": "Tomato",
        "detected_condition": "Tomato Yellow Leaf Curl Virus (TYLCV)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 25,
        "summary": (
            "Severe upward leaf curling, cupping, stunted bushy growth, and yellow leaf margins indicate "
            "tomato yellow leaf curl virus, transmitted by whiteflies."
        ),
        "recommended_action": [
            "Install yellow sticky traps (15 to 20 per acre) across the field to catch whiteflies.",
            "Spray neem oil (5 ml/L) or approved bio-insecticide to manage the whitefly vector.",
            "Rogue out and bury severely stunted diseased plants to prevent further spread.",
            "Use reflective silver mulch in future plantings to deter whitefly landings."
        ]
    },
    "Tomato___Tomato_mosaic_virus": {
        "crop_name": "Tomato",
        "detected_condition": "Tomato Mosaic Virus (Mottled Foliage)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 28,
        "summary": (
            "Alternating light and dark green mosaic patches, leaf blistering, and distorted foliage "
            "indicate tomato mosaic virus, easily spread by direct contact."
        ),
        "recommended_action": [
            "Rogue out and destroy infected plants immediately to prevent sap transmission.",
            "Disinfect hands and pruning tools with skim milk or mild soap solution.",
            "Do not smoke or use tobacco products near tomato crops.",
            "Select certified virus-resistant tomato seed varieties for subsequent seasons."
        ]
    },
    "Tomato___healthy": {
        "crop_name": "Tomato",
        "detected_condition": "Healthy Leaf Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 98,
        "summary": (
            "Tomato leaves display vigorous deep green coloration, stout stems, clean leaf surfaces, "
            "and absence of fungal spots or insect curling."
        ),
        "recommended_action": [
            "Continue balanced drip fertigation with potassium and calcium to support fruit set.",
            "Stake plants securely to keep fruit and foliage off the soil.",
            "Prune side suckers regularly to balance vegetative growth and fruit sizing.",
            "Inspect lower canopy leaves weekly for early signs of seasonal stress."
        ]
    },

    # ------------------ SUNFLOWER (ViT_Sunflower) ------------------
    "Sunflower___Downy_mildew": {
        "crop_name": "Sunflower",
        "detected_condition": "Downy Mildew (Foliar Chlorosis & White Growth)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 30,
        "summary": (
            "Pale yellow chlorosis along leaf veins with cottony white fungal growth underneath indicates "
            "sunflower downy mildew, which can cause severe seedling stunting."
        ),
        "recommended_action": [
            "Apply metalaxyl seed treatment or systemic foliar spray immediately to protect stand.",
            "Improve field drainage to prevent water stagnation in the root zone.",
            "Rogue out and safely destroy stunted, infected seedlings.",
            "Rotate the field with non-host crops like sorghum or chickpea next season."
        ]
    },
    "Sunflower___Gray_mold": {
        "crop_name": "Sunflower",
        "detected_condition": "Gray Mold (Botrytis Head & Leaf Rot)",
        "quality_grade": "Grade C (Health Risk)",
        "severity": "Critical",
        "base_score": 32,
        "summary": (
            "Water-soaked grayish-brown lesions covered with fuzzy gray fungal growth indicate botrytis "
            "gray mold, particularly harmful during humid or rainy flowering periods."
        ),
        "recommended_action": [
            "Apply iprodione or protective carbendazim spray at first appearance of rot.",
            "Remove and safely dispose of infected flower heads or leaves from the field.",
            "Maintain recommended plant spacing to facilitate rapid drying of flower heads.",
            "Harvest crop promptly once seeds reach physiological maturity."
        ]
    },
    "Sunflower___Healthy": {
        "crop_name": "Sunflower",
        "detected_condition": "Healthy Condition",
        "quality_grade": "Grade A (Prime)",
        "severity": "None",
        "base_score": 97,
        "summary": (
            "Sunflower plant exhibits robust green vegetative foliage, sturdy stem, and pristine ray "
            "petals with no signs of fungal spots or defoliation."
        ),
        "recommended_action": [
            "Ensure adequate boron application at ray floret opening for complete seed setting.",
            "Provide timely irrigation during critical budding and flowering stages.",
            "Scout flower heads for early signs of head-boring caterpillars.",
            "Keep field borders clean of competing weeds."
        ]
    },
    "Sunflower___Leaf_scars": {
        "crop_name": "Sunflower",
        "detected_condition": "Leaf Scars (Physical / Minor Cosmetic Marks)",
        "quality_grade": "Grade B (Early Attention)",
        "severity": "Mild",
        "base_score": 75,
        "summary": (
            "Minor mechanical leaf abrasions or healed scars from wind, hail, or minor insect feeding "
            "are observed. The underlying plant foliage and growth vigor remain sound."
        ),
        "recommended_action": [
            "Apply a mild foliar micronutrient spray to encourage rapid tissue healing.",
            "Maintain soil moisture to reduce wind stress on broad leaves.",
            "Avoid unnecessary mechanical operations that cause leaf tearing.",
            "Monitor foliage to ensure opportunistic fungal spores do not colonize abrasions."
        ]
    }
}

# Sunflower model short-label aliases
SUNFLOWER_SHORT_ALIASES: Dict[str, str] = {
    "downy mildew": "Sunflower___Downy_mildew",
    "gray mold": "Sunflower___Gray_mold",
    "healthy": "Sunflower___Healthy",
    "leaf scars": "Sunflower___Leaf_scars"
}


class LabelMapper:
    """Farmer-friendly translation mapper for vision model classes."""

    @classmethod
    def normalize_label(cls, raw_label: str, crop_hint: Optional[str] = None) -> str:
        """
        Normalize raw model label to match LABEL_DATABASE key.
        Handles variations like 'Tomato___Early_blight', 'tomato early blight',
        'Downy mildew' with crop_hint='sunflower', etc.
        """
        label_clean = raw_label.strip()

        # Direct match in database
        if label_clean in LABEL_DATABASE:
            return label_clean

        # Check sunflower short labels (e.g. 'Downy mildew', 'Gray mold', 'Healthy', 'Leaf scars')
        lower = label_clean.lower()
        if lower in SUNFLOWER_SHORT_ALIASES:
            return SUNFLOWER_SHORT_ALIASES[lower]

        if crop_hint and "sunflower" in crop_hint.lower():
            for key, db_key in SUNFLOWER_SHORT_ALIASES.items():
                if key in lower:
                    return db_key

        # Try case-insensitive matching in LABEL_DATABASE
        for db_key in LABEL_DATABASE:
            if db_key.lower() == lower:
                return db_key

        # Try replacing spaces/hyphens with underscores or vice versa
        norm = label_clean.replace(" ", "_").replace("-", "_")
        for db_key in LABEL_DATABASE:
            if db_key.lower() == norm.lower():
                return db_key

        # Partial matching by condition keyword if crop matches
        for db_key, data in LABEL_DATABASE.items():
            if data["crop_name"].lower() in lower and any(
                part.lower() in lower for part in db_key.split("___")[-1].split("_") if len(part) > 3
            ):
                return db_key

        return label_clean

    @classmethod
    def get_mapping(
        cls,
        raw_label: str,
        confidence: float = 1.0,
        crop_hint: Optional[str] = None
    ) -> CropAnalysisResult:
        """
        Map raw model label and confidence score to a clean, farmer-facing CropAnalysisResult.
        """
        # Sanitize and clamp confidence score (handles <0.0, >1.0, NaN, Inf, non-numeric)
        try:
            val = float(confidence)
            if math.isnan(val) or math.isinf(val):
                conf = 0.0
            else:
                conf = max(0.0, min(1.0, val))
        except (ValueError, TypeError):
            conf = 0.0

        norm_key = cls.normalize_label(raw_label, crop_hint=crop_hint)

        if norm_key in LABEL_DATABASE:
            info = LABEL_DATABASE[norm_key]
            crop_name = info["crop_name"]
            detected_condition = info["detected_condition"]
            quality_grade = info["quality_grade"]
            severity = info["severity"]
            base_score = info["base_score"]
            summary = info["summary"]
            recommended_action = list(info["recommended_action"])

            # Compute quality score modulated slightly by confidence
            # Healthy: score between 85 and 100
            # Mild/Moderate: score between 50 and 84
            # Critical: score between 0 and 49
            if severity == "None":
                # Healthy range: 85 - 100
                score = int(round(88 + 11 * conf))
                score = max(85, min(100, score))
            elif severity == "Mild":
                # Mild range: 65 - 84
                score = int(round(base_score + 10 * (1.0 - conf)))
                score = max(50, min(84, score))
            elif severity == "Moderate":
                # Moderate range: 50 - 64
                score = int(round(base_score - 5 + 10 * (1.0 - conf)))
                score = max(50, min(84, score))
            else:  # Critical
                # Critical range: 10 - 45
                score = int(round(base_score - 10 + 15 * (1.0 - conf)))
                score = max(0, min(49, score))

            return CropAnalysisResult(
                crop_name=crop_name,
                detected_condition=detected_condition,
                quality_grade=quality_grade,
                quality_score=score,
                confidence=round(conf, 4),
                severity=severity,
                summary=summary,
                recommended_action=recommended_action,
                raw_label=raw_label
            )

        # Fallback for completely unrecognized class
        fallback_crop = crop_hint.capitalize() if crop_hint else "General Crop"
        is_healthy = "healthy" in raw_label.lower()

        if is_healthy:
            return CropAnalysisResult(
                crop_name=fallback_crop,
                detected_condition="Healthy Leaf Condition",
                quality_grade="Grade A (Prime)",
                quality_score=90,
                confidence=round(conf, 4),
                severity="None",
                summary="The leaf foliage appears vigorous, green, and free from obvious fungal or insect distress.",
                recommended_action=[
                    "Maintain routine crop fertilization and regular watering.",
                    "Inspect plants weekly for any early signs of distress.",
                    "Ensure proper soil aeration and field sanitation."
                ],
                raw_label=raw_label
            )
        else:
            return CropAnalysisResult(
                crop_name=fallback_crop,
                detected_condition=f"Unclassified Leaf Condition ({raw_label.replace('___', ' ')})",
                quality_grade="Grade B (Early Attention)",
                quality_score=60,
                confidence=round(conf, 4),
                severity="Moderate",
                summary="Foliar irregularity observed. Timely monitoring and field hygiene are advised to safeguard yield.",
                recommended_action=[
                    "Prune affected leaves showing discoloration or spots.",
                    "Apply organic neem oil spray (1500 ppm) as a broad-spectrum preventive measure.",
                    "Ensure adequate field drainage and avoid wetting foliage during irrigation.",
                    "Consult local agricultural extension officer if symptoms spread."
                ],
                raw_label=raw_label
            )

    @classmethod
    def build_non_crop_result(cls, confidence: float = 0.95) -> CropAnalysisResult:
        """Construct a definitive non-crop rejection result when input is not an agricultural plant."""
        try:
            conf = max(0.0, min(1.0, float(confidence)))
        except (ValueError, TypeError):
            conf = 0.95

        return CropAnalysisResult(
            crop_name="Not a Crop or Plant",
            detected_condition="No Crop Detected",
            quality_grade="Not Applicable",
            quality_score=0,
            confidence=round(conf, 4),
            severity="None",
            summary="No agricultural crop, plant, leaf, or flower was detected in this picture. Please upload a clear photo focused on an agricultural plant or blossom.",
            recommended_action=[
                "Point your camera directly at a crop leaf, stem, or flower blossom.",
                "Ensure adequate natural lighting and keep the plant in sharp focus.",
                "Avoid photos of everyday objects, animals, vehicles, people, or plain backgrounds."
            ],
            is_crop=False,
            raw_label="Not a Crop or Plant"
        )

    @classmethod
    def list_supported_classes(cls) -> List[str]:
        """Return list of all 42 supported raw model keys."""
        return list(LABEL_DATABASE.keys())


def map_prediction_to_result(
    raw_label: str,
    confidence: float = 1.0,
    crop_hint: Optional[str] = None
) -> CropAnalysisResult:
    """Convenience helper to map prediction to CropAnalysisResult."""
    return LabelMapper.get_mapping(raw_label, confidence, crop_hint=crop_hint)
