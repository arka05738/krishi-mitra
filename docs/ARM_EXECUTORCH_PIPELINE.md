# Arm Bharat AI-SoC Challenge: ExecuTorch & Vision Dual-Pipeline Architecture

**Project**: Krishi Mitra (Offline Agricultural Advisory Platform)  
**Target Hardware**: Raspberry Pi 5 (Arm Cortex-A76, 4GB RAM) with optional Raspberry Pi AI HAT+ (Hailo-8L / Hailo-10H NPU) & RTX 3050 Local Field Station Server  
**Challenge Track**: Environment & Climate / Agriculture (Arm Education)

---

## 1. Architectural Overview: Separate Vision and Reasoning Pipelines

As specified in the **Bharat AI-SoC Challenge** guidelines:
> *"If a Hailo accelerator is used for vision workloads, vision models run through HailoRT on the Hailo NPU, while Llama runs through ExecuTorch on the Raspberry Pi Arm CPU. These are separate pipelines and should be clearly documented."*

Krishi Mitra strictly isolates these two compute workloads into decoupled pipelines to guarantee zero memory contention on the 4GB Raspberry Pi 5 and ensure maximum frames-per-second (FPS) and low-latency token generation:

```
+----------------------------------------------------------------------------------------------------+
|                                    KRISHI MITRA EDGE SYSTEM                                        |
+----------------------------------------------------------------------------------------------------+
                                                  │
                 ┌────────────────────────────────┴────────────────────────────────┐
                 ▼                                                                 ▼
   [PIPELINE A: VISION INFERENCE]                                   [PIPELINE B: REASONING & ADVISORY]
   Stage 1: SigLIP Crop Gatekeeper (Zero-shot)                      Runtime: ExecuTorch (Arm Reference)
   Stage 2: ViT Leaf & Blossom 42-Class Classifier                  Model:   Llama 3.2 1B / 3B-Instruct
   Target:  HailoRT on Hailo-8L NPU (or Host CUDA)                  Target:  Arm Cortex-A76 4x CPU Cores
   Output:  Crop Name, Condition, Grade, Severity                   Backend: XNNPACK + Arm KleidiAI Micro-kernels
                 │                                                                 │
                 └────────────────────────────────┬────────────────────────────────┘
                                                  ▼
                               [MULTI-TURN ICAR AGRONOMIC ADVISORY]
                               Language: English, Hindi, Bengali, Punjabi,
                                         Telugu, Tamil, Marathi
                               Offline Constraint: 100% Air-Gapped (Zero Cloud)
```

---

## 2. Pipeline A: Vision Inference Pipeline

### 2.1 Two-Stage Visual Health Diagnostic
1. **Stage 1 (Crop Gatekeeper)**:
   - Uses zero-shot vision features (`google/siglip-base-patch16-224`) to verify whether the captured photo contains plant foliage, crops, or agricultural flowers.
   - If a non-crop object (e.g., human, vehicle, gymnastics, indoor object) is presented, the gatekeeper immediately halts execution and returns a structured rejection notice, preventing false-positive disease classifications.
2. **Stage 2 (Disease & Quality Grading)**:
   - Evaluates the verified crop leaf/flower using a 38-class PlantVillage Vision Transformer (`kimcomehome/plantvillage-vit-leaf-disease`) and a 4-class Sunflower ViT (`YaswanthReddy23/ViT_Sunflower`).
   - Computes:
     - **Crop Identification**: Tomato, Potato, Corn, Wheat, Rice, Sunflower, Cotton, Apple, Chilli, etc.
     - **Condition Detection**: Early Blight, Late Blight, Common Rust, Powdery Mildew, Healthy Foliage.
     - **Quality Grade**: Grade A (Prime), Grade B (Attention Required), Grade C (Health Risk).
     - **Severity Level**: Healthy, Mild, Moderate, Critical.

### 2.2 Hailo-8L / Hailo-10H AI HAT+ Deployment (Optional NPU)
When deployed on a Raspberry Pi 5 equipped with the **Raspberry Pi AI HAT+**:
- The ViT models are compiled to HEF format using the Hailo Model Zoo:
  ```bash
  hailo parser onnx --hw-arch hailo8l vit_plantvillage.onnx
  hailo compiler vit_plantvillage.har --hw-arch hailo8l
  ```
- Execution runs via the lightweight `HailoRT` C++ / Python library, offloading 100% of matrix operations from the Cortex-A76 CPU and consuming only ~1.5W power.

---

## 3. Pipeline B: On-Device Llama ExecuTorch Pipeline

### 3.1 ExecuTorch as Reference Runtime
In compliance with the challenge mandate:
- **Model Family**: Llama 3.2 (1B-Instruct or 3B-Instruct)
- **Runtime**: PyTorch ExecuTorch v0.4+
- **Acceleration**:
  - **Arm KleidiAI**: Highly tuned vector micro-kernels for Arm Neon and Cortex-A76.
  - **XNNPACK**: Multithreaded FP16/INT4 CPU tensor execution.
- **Quantization**: INT4 weight-only quantization (`int4_awq` / `int4_weight_only`), compressing Llama 3.2-1B to under **1.15 GB RAM**, leaving ample memory headroom within the 4GB total RAM of the Raspberry Pi 5.

### 3.2 Exporting Llama 3.2 to ExecuTorch `.pte`
To export the Llama model for Arm deployment:
```bash
python llama/executorch/export_llama_pte.py \
    --model meta-llama/Llama-3.2-1B-Instruct \
    --quant int4 \
    --seqlen 512 \
    --outdir llama/executorch/exported_models
```

### 3.3 Executing On-Device Llama Service
On the Raspberry Pi 5:
```bash
# Start the local ExecuTorch inference microservice
python llama/executorch/service.py
# Listening on http://127.0.0.1:8008/generate
```

---

## 4. Grounded Multilingual Agronomic Advisory & Soil Engine

1. **ICAR Grounded Retrieval**:
   - 122 indexed chunks from Indian Council of Agricultural Research (ICAR) Packages of Practices, fertilizer manuals, and PM-KISAN/PMFBY guidelines stored in local ChromaDB.
2. **STCR 12-Parameter Soil Health Card Engine**:
   - Calculates targeted commercial dosages for Urea (46% N), DAP (18-46-0), SSP (16% P), and MOP (60% K).
   - Enforces chemical safety rules: Strict prohibition against tank-mixing Zinc Sulphate with DAP/SSP to prevent zinc phosphate precipitation.
3. **Multilingual Localized Support**:
   - Complete offline translations across 7 Indian languages: English, Hindi (हिन्दी), Bengali (বাংলা), Punjabi (ਪੰਜਾਬੀ), Telugu (తెలుగు), Tamil (தமிழ்), Marathi (मराठी).
   - Allows rural farmers with zero English proficiency to inspect diagnoses, calculate fertilizers, and read scheme benefits.

---

## 5. Verification & Benchmark Checklist

| Benchmark Requirement | Status | Architecture Details |
|---|---|---|
| **Llama Model Used** | **COMPLIANT** | Llama 3.2 (1B/3B-Instruct) for reasoning |
| **ExecuTorch Reference Runtime** | **COMPLIANT** | Deployed with XNNPACK + Arm KleidiAI on Cortex-A76 |
| **Separate Vision & LLaMA Pipelines** | **COMPLIANT** | Documented & decoupled; ViT / SigLIP vs. ExecuTorch |
| **Target Hardware: Raspberry Pi 5** | **COMPLIANT** | 4GB RAM budget strictly preserved (<1.2GB for model) |
| **Disease & Pest Detection** | **COMPLIANT** | 42 agricultural plant and blossom classes |
| **Severity Level Classification** | **COMPLIANT** | None, Mild, Moderate, Critical |
| **Treatment & Action Guidance** | **COMPLIANT** | Immediate, chemical (dosage/acre), organic, preventive |
| **Multilingual Local Languages** | **COMPLIANT** | English, Hindi, Bengali, Punjabi, Telugu, Tamil, Marathi |
| **Fully Offline (Zero Internet)** | **COMPLIANT** | 100% air-gapped local Wi-Fi hotspot operation |
