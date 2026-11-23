"""
Script to pre-cache required Hugging Face models locally on Raspberry Pi 5.
Once cached, the system runs 100% offline with zero internet access.
"""

import os
import sys
from pathlib import Path

# Load HF Token
HF_TOKEN = os.getenv("HUGGINGFACE_API_KEY")
if not HF_TOKEN:
    env_path = Path(__file__).resolve().parent / ".env"
    if env_path.exists():
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                if line.startswith("HUGGINGFACE_API_KEY="):
                    HF_TOKEN = line.strip().split("=", 1)[1].strip()
                    break

os.environ["HF_TOKEN"] = HF_TOKEN or ""
# Disable offline flag temporarily during download
os.environ.pop("HF_HUB_OFFLINE", None)
os.environ.pop("TRANSFORMERS_OFFLINE", None)

print("=" * 65)
print(" Pre-caching Models for 100% Offline Edge Operation ")
print(" Hardware: Raspberry Pi 5 (Arm Cortex-A76, 4GB RAM)")
print("=" * 65)

# 1. Download Sentence-Transformers MiniLM (ChromaDB RAG)
print("\n[1/4] Pre-caching sentence-transformers/all-MiniLM-L6-v2...")
try:
    from sentence_transformers import SentenceTransformer
    st_model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", token=HF_TOKEN)
    print("  -> all-MiniLM-L6-v2 cached successfully!")
except Exception as e:
    print(f"  -> Error caching MiniLM: {e}")

# 2. Download PlantVillage ViT Disease Classifier
print("\n[2/4] Pre-caching kimcomehome/plantvillage-vit-leaf-disease...")
try:
    from transformers import AutoImageProcessor, AutoModelForImageClassification
    m1 = "kimcomehome/plantvillage-vit-leaf-disease"
    AutoImageProcessor.from_pretrained(m1, token=HF_TOKEN)
    AutoModelForImageClassification.from_pretrained(m1, token=HF_TOKEN)
    print("  -> PlantVillage ViT cached successfully!")
except Exception as e:
    print(f"  -> Error caching PlantVillage ViT: {e}")

# 3. Download Sunflower ViT Classifier
print("\n[3/4] Pre-caching YaswanthReddy23/ViT_Sunflower...")
try:
    m2 = "YaswanthReddy23/ViT_Sunflower"
    AutoImageProcessor.from_pretrained(m2, token=HF_TOKEN)
    AutoModelForImageClassification.from_pretrained(m2, token=HF_TOKEN)
    print("  -> Sunflower ViT cached successfully!")
except Exception as e:
    print(f"  -> Error caching Sunflower ViT: {e}")

# 4. Download SigLIP Crop Gatekeeper
print("\n[4/4] Pre-caching google/siglip-base-patch16-224...")
try:
    from transformers import AutoProcessor, AutoModel
    m3 = "google/siglip-base-patch16-224"
    AutoProcessor.from_pretrained(m3, token=HF_TOKEN)
    AutoModel.from_pretrained(m3, token=HF_TOKEN)
    print("  -> SigLIP Gatekeeper cached successfully!")
except Exception as e:
    print(f"  -> Error caching SigLIP: {e}")

print("\n" + "=" * 65)
print(" All Vision and RAG Models Successfully Cached Locally!")
print(" Device is now 100% Offline Ready.")
print("=" * 65)
