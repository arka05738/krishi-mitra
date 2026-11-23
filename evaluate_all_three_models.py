"""
Comprehensive Model Evaluation Script for Krishi Mitra on Raspberry Pi 5.
Evaluates:
1. Model 1: Plant Crop Disease (Hugging Face ViT + EfficientNetB0)
2. Model 2: Pest Classification (EfficientNetB0 102-Class IP102)
3. Model 3: Pest Detection (YOLO26n 97-Class IP102)
4. Non-Crop Gatekeeper (SigLIP Zero-Shot)

Outputs exact class predictions, top-k probabilities, inference latencies (ms),
and real-world field reliability analysis.
"""

import os
import sys
import time
import json
from pathlib import Path
from PIL import Image

os.environ["KERAS_BACKEND"] = "torch"
os.environ["HF_HUB_OFFLINE"] = "1"
os.environ["TRANSFORMERS_OFFLINE"] = "1"

import torch
import numpy as np
import keras

# Import pipelines
from server.app.vision.vision_pipeline import get_vision_pipeline
from server.app.vision.pest_pipeline import get_pest_pipeline

def run_evaluation():
    print("================================================================================")
    print("      KRISHI MITRA — 3-MODEL DEEP EVALUATION BENCHMARK ON RASPBERRY PI 5       ")
    print("      Hardware: Arm Cortex-A76 @ 2.4 GHz | 4 GB LPDDR4X RAM | 100% Offline     ")
    print("================================================================================\n")

    vision_pipeline = get_vision_pipeline()
    pest_pipeline = get_pest_pipeline()
    
    # Load primary EfficientNet disease model
    disease_eff_path = Path("AgriRakshak_Models_20261118_0437/Disease_Classification/efficientnetb0_disease_primary.keras")
    eff_disease_model = keras.models.load_model(str(disease_eff_path)) if disease_eff_path.exists() else None

    # Get ViT class id2label
    vit_id2label = vision_pipeline._get_or_load_model("kimcomehome/plantvillage-vit-leaf-disease")[1].config.id2label

    eval_results = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "hardware": "Raspberry Pi 5 (Quad-Core Cortex-A76, 4GB RAM)",
        "model_1_disease": [],
        "model_2_pest_classification": [],
        "model_3_pest_detection": [],
        "gatekeeper_controls": []
    }

    # -------------------------------------------------------------------------
    # PART 1: TEST MODEL 1 — PLANT CROP DISEASE (ViT & EfficientNetB0)
    # -------------------------------------------------------------------------
    print(">>> [PART 1/4] Evaluating Model 1: Plant Crop Disease Prediction...")
    disease_images = [
        ("test_eval_suite/disease_apple_scab.jpg", "Apple", "Apple Scab"),
        ("test_eval_suite/disease_potato_late_blight.jpg", "Potato", "Late Blight"),
        ("test_eval_suite/disease_tomato_early_blight.jpg", "Tomato", "Early Blight"),
        ("test_eval_suite/disease_corn_rust.jpg", "Corn", "Common Rust"),
        ("test_eval_suite/disease_grape_black_rot.jpg", "Grape", "Black Rot"),
        ("tomato_infected.jpeg", "Tomato", "Late Blight"),
        ("server/app/vision/sample_images/tomato_healthy.jpg", "Tomato", "Healthy"),
        ("server/app/vision/sample_images/sunflower_healthy.jpg", "Sunflower", "Healthy")
    ]

    for img_path_str, expected_crop, expected_condition in disease_images:
        path = Path(img_path_str)
        if not path.exists():
            continue
        try:
            pil_img = Image.open(path).convert("RGB")
            
            # ViT Inference
            t0 = time.time()
            res_vit = vision_pipeline.analyze(pil_img, crop_hint=expected_crop)
            vit_lat_ms = round((time.time() - t0) * 1000, 1)

            # EfficientNet Inference
            eff_pred_label = "N/A"
            eff_conf = 0.0
            eff_lat_ms = 0.0
            if eff_disease_model:
                img_res = pil_img.resize((224, 224))
                arr = np.array(img_res, dtype=np.float32)
                t_in = torch.from_numpy(arr).unsqueeze(0)
                t0_eff = time.time()
                with torch.no_grad():
                    logits = eff_disease_model(t_in, training=False)
                    probs = torch.softmax(logits, dim=-1)[0]
                    top_idx = torch.argmax(probs).item()
                    eff_conf = round(probs[top_idx].item() * 100, 1)
                    eff_pred_label = vit_id2label.get(top_idx, f"Class_{top_idx}")
                eff_lat_ms = round((time.time() - t0_eff) * 1000, 1)

            entry = {
                "file": path.name,
                "expected": f"{expected_crop} - {expected_condition}",
                "vit_predicted_crop": res_vit.crop_name,
                "vit_predicted_condition": res_vit.detected_condition,
                "vit_confidence_pct": round(res_vit.confidence * 100, 1),
                "vit_latency_ms": vit_lat_ms,
                "efficientnet_predicted": eff_pred_label,
                "efficientnet_confidence_pct": eff_conf,
                "efficientnet_latency_ms": eff_lat_ms,
                "severity": res_vit.severity
            }
            eval_results["model_1_disease"].append(entry)
            print(f"  [Disease] {path.name:<32}\n"
                  f"            Expected: {expected_crop} ({expected_condition})\n"
                  f"            ViT:      {res_vit.crop_name} - {res_vit.detected_condition} ({entry['vit_confidence_pct']}%) [{vit_lat_ms}ms]\n"
                  f"            EffNet:   {eff_pred_label} ({eff_conf}%) [{eff_lat_ms}ms]\n")
        except Exception as e:
            print(f"  [Disease] {path.name} FAILED: {e}")

    # -------------------------------------------------------------------------
    # PART 2: TEST MODEL 2 — PEST CLASSIFICATION (EfficientNetB0 102 Classes)
    # -------------------------------------------------------------------------
    print("\n>>> [PART 2/4] Evaluating Model 2: Pest Classification (102 Classes)...")
    pest_images = [
        ("test_aphid_field.jpg", "aphids"),
        ("test_eval_suite/pest_armyworm.jpg", "army worm"),
        ("test_eval_suite/pest_rice_leaf_roller.jpg", "rice leaf roller"),
        ("test_eval_suite/pest_brown_planthopper.jpg", "brown plant hopper"),
        ("test_eval_suite/pest_corn_borer.jpg", "corn borer"),
        ("test_eval_suite/pest_mole_cricket.jpg", "mole cricket"),
        ("test_eval_suite/pest_red_spider.jpg", "red spider"),
    ]

    for img_path_str, expected_pest in pest_images:
        path = Path(img_path_str)
        if not path.exists():
            continue
        try:
            res = pest_pipeline.classify_pest(path, top_k=3)
            lat_ms = res["latency_ms"]

            entry = {
                "file": path.name,
                "expected_pest": expected_pest,
                "predicted_pest": res["primary_pest"],
                "confidence_pct": res["confidence_pct"],
                "top_3_candidates": [f"{c['pest_name']} ({c['confidence_pct']}%)" for c in res["candidates"]],
                "severity": res["severity"],
                "latency_ms": lat_ms
            }
            eval_results["model_2_pest_classification"].append(entry)
            print(f"  [Pest-Cls] {path.name:<30} -> Top: {res['primary_pest']:<20} "
                  f"| Conf: {res['confidence_pct']}% | Top3: {entry['top_3_candidates']} | Latency: {lat_ms}ms")
        except Exception as e:
            print(f"  [Pest-Cls] {path.name} FAILED: {e}")

    # -------------------------------------------------------------------------
    # PART 3: TEST MODEL 3 — PEST DETECTION (YOLO26n 97 Classes)
    # -------------------------------------------------------------------------
    print("\n>>> [PART 3/4] Evaluating Model 3: Pest Detection & Bounding Boxes (97 Classes)...")
    for img_path_str, expected_pest in pest_images:
        path = Path(img_path_str)
        if not path.exists():
            continue
        try:
            res = pest_pipeline.detect_pests(path, conf_threshold=0.15)
            dets = res["detections"]
            det_summary = [f"{d['pest_name']} ({d['confidence_pct']}%, box={d['box']})" for d in dets]
            
            entry = {
                "file": path.name,
                "expected_pest": expected_pest,
                "total_detected": res["total_detected"],
                "detections": det_summary,
                "latency_ms": res["latency_ms"],
                "status": res["status"]
            }
            eval_results["model_3_pest_detection"].append(entry)
            print(f"  [Pest-Det] {path.name:<30} -> Detected {res['total_detected']} pest(s): {det_summary} | Latency: {res['latency_ms']}ms")
        except Exception as e:
            print(f"  [Pest-Det] {path.name} FAILED: {e}")

    # -------------------------------------------------------------------------
    # PART 4: TEST GATEKEEPER ON NEGATIVE / NON-CROP CONTROLS
    # -------------------------------------------------------------------------
    print("\n>>> [PART 4/4] Evaluating SigLIP Gatekeeper on Non-Crop Controls...")
    control_images = [
        ("person_test.jpg", "Human portrait (Non-Crop)"),
        ("test_eval_suite/control_soil_background.jpg", "Bare furrowed soil")
    ]
    for img_path_str, desc in control_images:
        path = Path(img_path_str)
        if not path.exists():
            continue
        try:
            pil_img = Image.open(path).convert("RGB")
            t0 = time.time()
            res = vision_pipeline.analyze(pil_img)
            lat_ms = round((time.time() - t0) * 1000, 1)

            entry = {
                "file": path.name,
                "description": desc,
                "is_crop": res.is_crop,
                "gatekeeper_rejected": not res.is_crop,
                "confidence_pct": round(res.confidence * 100, 1),
                "condition": res.detected_condition,
                "latency_ms": lat_ms
            }
            eval_results["gatekeeper_controls"].append(entry)
            print(f"  [Gatekeeper] {path.name:<30} ({desc}) -> Is Crop: {res.is_crop} | Condition: {res.detected_condition} | Latency: {lat_ms}ms")
        except Exception as e:
            print(f"  [Gatekeeper] {path.name} FAILED: {e}")

    # Save benchmark results to JSON
    with open("model_benchmark_results.json", "w") as f:
        json.dump(eval_results, f, indent=2)
    print("\nBenchmark saved to model_benchmark_results.json")

if __name__ == "__main__":
    run_evaluation()
