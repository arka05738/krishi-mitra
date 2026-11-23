"""
Download authentic agricultural field test images from Wikimedia Commons for:
1. Plant crop disease classes
2. Pest classes
3. Ambiguous/challenging real-world conditions
"""
import os
import json
import urllib.request
import socket
from pathlib import Path

# Force IPv4
_orig = socket.getaddrinfo
socket.getaddrinfo = lambda host, port, family=0, type=0, proto=0, flags=0: _orig(host, port, socket.AF_INET, type, proto, flags)

EVAL_DIR = Path("test_eval_suite")
EVAL_DIR.mkdir(exist_ok=True)

TARGET_CLASSES = [
    # Diseases
    ("disease", "apple_scab", "Venturia inaequalis apple scab leaf"),
    ("disease", "potato_late_blight", "Phytophthora infestans potato late blight"),
    ("disease", "tomato_early_blight", "Alternaria solani tomato early blight"),
    ("disease", "corn_rust", "Puccinia sorghi corn common rust"),
    ("disease", "grape_black_rot", "Guignardia bidwellii grape black rot"),
    
    # Pests
    ("pest", "aphids", "Aphis fabae aphid colony leaf"),
    ("pest", "armyworm", "Spodoptera frugiperda fall armyworm larva"),
    ("pest", "rice_leaf_roller", "Cnaphalocrocis medinalis rice leaf roller"),
    ("pest", "brown_planthopper", "Nilaparvata lugens brown planthopper"),
    ("pest", "corn_borer", "Ostrinia nubilalis European corn borer"),
    ("pest", "mole_cricket", "Gryllotalpa mole cricket"),
    ("pest", "red_spider", "Tetranychus urticae red spider mite leaf"),
    
    # Controls / Ambiguous
    ("control", "healthy_leaf", "healthy green leaf close up"),
    ("control", "soil_background", "agricultural soil field furrow"),
]

headers = {'User-Agent': 'KrishiMitraAgriEvalBot/1.0 (krishimitra@armchallenge.org)'}

for category, label, query in TARGET_CLASSES:
    out_path = EVAL_DIR / f"{category}_{label}.jpg"
    if out_path.exists():
        print(f"Skipping {out_path.name} (already exists)")
        continue
    
    api_url = f"https://commons.wikimedia.org/w/api.php?action=query&generator=search&gsrnamespace=6&gsrsearch={urllib.parse.quote(query)}&gsrlimit=5&prop=imageinfo&iiprop=url|mime|size&format=json"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode())
            pages = data.get("query", {}).get("pages", {})
            downloaded = False
            for pid, p in pages.items():
                info = p.get("imageinfo", [{}])[0]
                mime = info.get("mime", "")
                img_url = info.get("url", "")
                size = info.get("size", 0)
                if ("image/jpeg" in mime or "image/png" in mime) and img_url and size < 5_000_000:
                    # Download image
                    img_req = urllib.request.Request(img_url, headers=headers)
                    with urllib.request.urlopen(img_req, timeout=12) as img_resp:
                        content = img_resp.read()
                        with open(out_path, "wb") as f:
                            f.write(content)
                        print(f"Downloaded [{category}] {label}: {len(content)} bytes from {p.get('title')}")
                        downloaded = True
                        break
            if not downloaded:
                print(f"Could not find suitable jpeg/png for query: {query}")
    except Exception as e:
        print(f"Error downloading {label}: {e}")

print("Download complete. Files in", EVAL_DIR, ":", len(list(EVAL_DIR.glob('*'))))
