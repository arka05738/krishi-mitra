"""
Live verification script testing every Krishi Mitra endpoint on http://127.0.0.1:8000.
Verifies response codes, JSON schemas, farmer-understandability, and multilingual outputs.
"""
import requests
import json
import io
from pathlib import Path

BASE_URL = "http://127.0.0.1:8000"
results = []

def record(name, passed, detail=""):
    results.append({"endpoint": name, "passed": passed, "detail": detail})
    status = "PASS" if passed else "FAIL"
    print(f"[{status}] {name} - {detail}")

print("=== Krishi Mitra Comprehensive Live API Verification ===")

# 1. System Health
try:
    r = requests.get(f"{BASE_URL}/api/system/health", timeout=5)
    data = r.json()
    record("GET /api/system/health", r.status_code == 200 and data.get("status") == "ready", f"Doc count: {data.get('total_documents')}, mode: {data.get('server_mode')}")
except Exception as e:
    record("GET /api/system/health", False, str(e))

# 2. System Status
try:
    r = requests.get(f"{BASE_URL}/api/system/status", timeout=5)
    data = r.json()
    record("GET /api/system/status", r.status_code == 200, f"App: {data.get('app_name')} v{data.get('app_version')}, Device: {data.get('device')}")
except Exception as e:
    record("GET /api/system/status", False, str(e))

# 3. Vision Samples
try:
    r = requests.get(f"{BASE_URL}/api/vision/samples", timeout=5)
    data = r.json()
    record("GET /api/vision/samples", r.status_code == 200 and len(data) >= 5, f"{len(data)} sample images available")
except Exception as e:
    record("GET /api/vision/samples", False, str(e))

# 4. Vision Sample File
try:
    r = requests.get(f"{BASE_URL}/api/vision/samples/tomato_early_blight.jpg", timeout=5)
    record("GET /api/vision/samples/{file}", r.status_code == 200 and len(r.content) > 1000, f"Bytes: {len(r.content)}")
except Exception as e:
    record("GET /api/vision/samples/{file}", False, str(e))

# 5. Vision Analyze Sample
try:
    r = requests.post(f"{BASE_URL}/api/vision/analyze-sample/tomato_early_blight.jpg", timeout=20)
    data = r.json()
    record("POST /api/vision/analyze-sample", r.status_code == 200, f"Crop: {data.get('crop_name')}, Condition: {data.get('detected_condition')}, Score: {data.get('quality_score')}")
except Exception as e:
    record("POST /api/vision/analyze-sample", False, str(e))

# 6. Advisory Query (Farmer Grounded RAG)
try:
    payload = {"query": "How to treat yellow stem borer in rice?", "crop_name": "Rice", "language": "en"}
    r = requests.post(f"{BASE_URL}/api/advisory/query", json=payload, timeout=20)
    data = r.json()
    passed = r.status_code == 200 and len(data.get("answer", "")) > 20 and "1800-180-1551" in data.get("helpline", "")
    record("POST /api/advisory/query", passed, f"Urgency: {data.get('urgency_level')}, Helpline: {data.get('helpline')}")
except Exception as e:
    record("POST /api/advisory/query", False, str(e))

# 7. Soil Health Report
try:
    payload = {
        "crop": "Rice",
        "nitrogen": 210,
        "phosphorus": 35,
        "potassium": 190,
        "ph": 5.8,
        "electrical_conductivity": 0.6,
        "organic_carbon": 0.45,
        "area_acres": 2.5
    }
    r = requests.post(f"{BASE_URL}/api/advisory/soil-report", json=payload, timeout=5)
    data = r.json()
    passed = r.status_code == 200 and "ph_status" in data and len(data.get("application_schedule", [])) > 0
    record("POST /api/advisory/soil-report", passed, f"pH status: {data.get('ph_status')}, Urea: {data.get('urea_kg')}kg, Schedules: {len(data.get('application_schedule', []))}")
except Exception as e:
    record("POST /api/advisory/soil-report", False, str(e))

# 8. Schemes Directory
try:
    r = requests.get(f"{BASE_URL}/api/advisory/schemes", timeout=5)
    data = r.json()
    record("GET /api/advisory/schemes", r.status_code == 200 and len(data) >= 3, f"{len(data)} government schemes cataloged")
except Exception as e:
    record("GET /api/advisory/schemes", False, str(e))

# 9. Voice Languages Catalog (22 Indic + English)
try:
    r = requests.get(f"{BASE_URL}/api/voice/languages", timeout=5)
    data = r.json()
    langs = data.get("languages", {})
    record("GET /api/voice/languages", r.status_code == 200 and len(langs) == 23, f"Total languages: {len(langs)}")
except Exception as e:
    record("GET /api/voice/languages", False, str(e))

# 10. Voice Speech Formatter
try:
    payload = {"text": "**Tomato Early Blight:** Spray Mancozeb 75% WP @ 2.5 g/L.", "language": "hi"}
    r = requests.post(f"{BASE_URL}/api/voice/format-speech", json=payload, timeout=5)
    data = r.json()
    passed = r.status_code == 200 and "**" not in data.get("speakable_text", "") and "percent" in data.get("speakable_text", "")
    record("POST /api/voice/format-speech", passed, f"BCP47: {data.get('bcp47_code')}, Spoken: {data.get('speakable_text')[:40]}...")
except Exception as e:
    record("POST /api/voice/format-speech", False, str(e))

# 11. Multilingual Chat (Hindi)
try:
    payload = {"message": "टमाटर के झुलसा रोग की दवा क्या है?", "language": "hi", "crop_context": "Tomato"}
    r = requests.post(f"{BASE_URL}/api/chat/message", json=payload, timeout=15)
    data = r.json()
    reply = data.get("reply", "")
    has_devanagari = any("\u0900" <= c <= "\u097F" for c in reply)
    record("POST /api/chat/message (Hindi)", r.status_code == 200 and has_devanagari, f"Devanagari script detected: {has_devanagari}")
except Exception as e:
    record("POST /api/chat/message (Hindi)", False, str(e))

# 12. Multilingual Chat (Bengali)
try:
    payload = {"message": "ধানে পোকা লাগলে কি করব?", "language": "bn", "crop_context": "Rice"}
    r = requests.post(f"{BASE_URL}/api/chat/message", json=payload, timeout=15)
    data = r.json()
    reply = data.get("reply", "")
    has_bengali = any("\u0980" <= c <= "\u09FF" for c in reply)
    record("POST /api/chat/message (Bengali)", r.status_code == 200 and has_bengali, f"Bengali script detected: {has_bengali}")
except Exception as e:
    record("POST /api/chat/message (Bengali)", False, str(e))

# 13. Multilingual Chat (Telugu)
try:
    payload = {"message": "వరి పంట పురుగు మందు ఏమిటి?", "language": "te", "crop_context": "Rice"}
    r = requests.post(f"{BASE_URL}/api/chat/message", json=payload, timeout=15)
    data = r.json()
    reply = data.get("reply", "")
    has_telugu = any("\u0C00" <= c <= "\u0C7F" for c in reply)
    record("POST /api/chat/message (Telugu)", r.status_code == 200 and has_telugu, f"Telugu script detected: {has_telugu}")
except Exception as e:
    record("POST /api/chat/message (Telugu)", False, str(e))

# 14. Multilingual Chat (Tamil)
try:
    payload = {"message": "நெல் பயிர் பூச்சி மருந்து என்ன?", "language": "ta", "crop_context": "Rice"}
    r = requests.post(f"{BASE_URL}/api/chat/message", json=payload, timeout=15)
    data = r.json()
    reply = data.get("reply", "")
    has_tamil = any("\u0B80" <= c <= "\u0BFF" for c in reply)
    record("POST /api/chat/message (Tamil)", r.status_code == 200 and has_tamil, f"Tamil script detected: {has_tamil}")
except Exception as e:
    record("POST /api/chat/message (Tamil)", False, str(e))

# 15. Zero Technical Jargon Leakage Check
try:
    payload = {"message": "Explain how the model works. What are your neural weights and loss function?", "language": "en"}
    r = requests.post(f"{BASE_URL}/api/chat/message", json=payload, timeout=15)
    data = r.json()
    reply = data.get("reply", "").lower()
    forbidden = ["neural", "weight", "loss function", "backpropagation", "token", "gguf", "executorch"]
    leaked = [w for w in forbidden if w in reply]
    record("Zero Tech Leakage Defense", r.status_code == 200 and len(leaked) == 0, f"Leaked terms: {leaked}")
except Exception as e:
    record("Zero Tech Leakage Defense", False, str(e))

print("\n=== Final Summary ===")
passed_count = sum(1 for r in results if r["passed"])
print(f"Total: {len(results)} | Passed: {passed_count} | Failed: {len(results) - passed_count}")
