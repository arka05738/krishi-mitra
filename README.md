# Krishi Mitra (कृषि मित्र / কৃষি মিত্র)
### 100% Offline AI-SoC Edge Agricultural Advisory & Plant Pathology Platform for Arm Platforms

[![Target Hardware](https://img.shields.io/badge/Hardware-Raspberry_Pi_5_(Arm_Cortex--A76)-red.svg?logo=raspberrypi)](https://www.raspberrypi.com/)
[![100% Offline](https://img.shields.io/badge/Air--Gapped-100%25_Offline_(Zero_WAN)-success.svg)](TEST_READY.md)
[![Runtime](https://img.shields.io/badge/Runtime-ExecuTorch_INT4_+_XNNPACK-orange.svg)](https://pytorch.org/executorch/)
[![Reasoning Core](https://img.shields.io/badge/LLM-Llama_3.2_1B_Instruct-purple.svg)](https://ai.meta.com/llama/)
[![Vector RAG](https://img.shields.io/badge/RAG-122_ICAR_Packages_(ChromaDB)-blue.svg)](Advisory%20data/)
[![Air-Gap Tests](https://img.shields.io/badge/Air--Gap_E2E_Tests-93%2F93_Passed-brightgreen.svg)](TEST_READY.md)
[![License](https://img.shields.io/badge/License-Apache_2.0-green.svg)](LICENSE)
[![Live Web Dashboard](https://img.shields.io/badge/Web_Dashboard-GitHub_Pages-blue.svg)](https://arka05738.github.io/krishi-mitra/)

---

## 1. Executive Summary & Problem Statement

Smallholder farmers in India cultivate more than 86% of operational agricultural holdings. According to published field research from the Indian Council of Agricultural Research (ICAR), unmitigated plant diseases, fungal blights, and insect infestations destroy 15% to 25% of annual harvest yields. 

In remote farming villages, two major barriers prevent farmers from accessing modern digital agronomy:
1. **The Rural Connectivity Divide**: Cellular data is frequently unavailable, intermittent, or prohibitive in cost. Cloud-dependent agricultural apps fail in air-gapped field environments.
2. **Overburdened Agricultural Extension**: Krishi Vigyan Kendra (KVK) extension officers manage severe caseloads, with extension-to-farmer ratios often exceeding 1:1,000.

**Krishi Mitra** is an on-device, fully air-gapped artificial intelligence field station engineered specifically for Arm Cortex-A76 SoCs (Raspberry Pi 5) and Arm-based smartphones. It operates **100% offline with zero internet access, zero SIM card dependencies, and zero recurring cloud subscription fees**. The platform delivers real-time visual crop pathology, insect pest detection with Integrated Pest Management (IPM), 12-parameter Soil Health Card fertilizer dosage calculation, and interactive agronomic advisory synthesized in local scripts across 22 Scheduled Indian Languages plus English.

---

## 2. 100% Offline & Air-Gapped Architectural Guarantee

Krishi Mitra is designed from the ground up for strict, zero-trust air-gapped deployment:

* **Zero Outbound WAN Traffic**: The platform requires no internet connection during field operations. An automated socket-level network monitor (`tests/e2e_offline_test.py`) intercepts all system network calls and verifies **0.0 outbound bytes** and zero external DNS resolutions.
* **100% On-Device Neural Compute**:
  * **Visual Pathology**: SigLIP zero-shot gatekeeper, 38-class PlantVillage ViT, 4-class Sunflower ViT, 97-class YOLO26n pest detector, and 102-class EfficientNetB0 classifier execute locally on CPU/NPU.
  * **Agronomic Reasoning**: Meta's Llama 3.2 1B-Instruct executes on-device via PyTorch's ExecuTorch runtime with 4-bit quantization (`int4_weight_only`), accelerated by Arm KleidiAI and XNNPACK micro-kernels.
  * **Vector RAG**: ChromaDB SQLite store containing 122 indexed ICAR/SAU Package of Practices is queried locally using embedded `all-MiniLM-L6-v2` vectors in ~18 ms.
  * **Speech I/O**: Offline Whisper transcription and local native speech synthesis.
* **Local Hotspot Field Station**: The Raspberry Pi 5 broadcasts its own offline Wi-Fi access point (`192.168.5.200:8000`). Up to 20 farmers or extension workers can connect simultaneously with standard smartphone web browsers with zero cellular data charges.
* **One-Time Pre-Caching**: Running `download_offline_models.py` and `llama/download_llama.py` once caches all weights locally. Thereafter, the field unit runs indefinitely air-gapped.

---

## 3. Decoupled Dual-Pipeline Architecture

In strict compliance with the **Arm Bharat AI-SoC Challenge** reference specification, the computational workload is bifurcated into two independent pipelines. This decoupled design ensures real-time deterministic computer vision throughput while running on-device generative reasoning without memory or thermal contention on 4GB hardware.

```
+──────────────────────────────────────────────────────────────────────────────────────────────────────────+
|                                    KRISHI MITRA SYSTEM ARCHITECTURE                                       |
+──────────────────────────────────────────────────────────────────────────────────────────────────────────+

    [FARMER EDGE CLIENT]                                 [LOCAL EDGE AI FIELD STATION (PI 5 / ARM64)]
    • Progressive Web App (React 19 + TypeScript)        • Local Station Server (FastAPI :8000)
    • High-Contrast Rural Daylight Theme                 • Air-Gap Network Sandbox (Zero WAN Calls)
    • Touch & Offline Speech I/O (Whisper/Coqui)         • Local Hotspot Broadcast (192.168.5.200:8000)
    • 22 Scheduled Indian Languages + English                           │
                    │                                                   ▼
                    │ Local Wi-Fi Hotspot               ┌───────────────────────────────────────────────┐
                    └──────────────────────────────────►│              PIPELINE A: VISION ENGINE        │
                                                        │ • Stage 1: SigLIP Non-Crop Gatekeeper         │
                                                        │ • Stage 2A: 38-Class PlantVillage ViT         │
                                                        │ • Stage 2B: 4-Class Sunflower ViT             │
                                                        │ • Stage 3: IP102 97-Class YOLO + EfficientNet │
                                                        │ • Severity & Commercial Dosage Synthesizer    │
                                                        └───────────────────────────────────────────────┘
                                                                        │
                                                                        ▼
                                                        ┌───────────────────────────────────────────────┐
                                                        │          PIPELINE B: REASONING & RAG          │
                                                        │ • ChromaDB Vector Store (122 ICAR Packages)   │
                                                        │ • Sentence-Transformers all-MiniLM-L6-v2      │
                                                        │ • ExecuTorch INT4 Llama 3.2-1B-Instruct (:8008│
                                                        │ • Arm KleidiAI / XNNPACK Micro-Kernels        │
                                                        │ • Rural Jargon Purger & Plain-Language Engine │
                                                        └───────────────────────────────────────────────┘
                                                                        │
                                                                        ▼
                                                        ┌───────────────────────────────────────────────┐
                                                        │       SOIL HEALTH & GOVERNMENT SCHEMES        │
                                                        │ • 12-Parameter STCR Fertilizer Formulator     │
                                                        │ • PM-KISAN, PMFBY (72h Rule), KCC Offline DB  │
                                                        └───────────────────────────────────────────────┘
```

### Pipeline A — Edge Vision & Pest Diagnostic Engine
1. **Stage 1 (Zero-Shot Crop Gatekeeper)**: Employs `google/siglip-base-patch16-224` to compute cosine similarity against agricultural and non-agricultural prompt sets. Any image lacking crop foliage, stems, petals, or field pests (e.g. human selfies, domestic animals, machinery, indoor objects) is rejected immediately with an informative rural guidance message before invoking downstream classifiers.
2. **Stage 2 (Disease & Blossom Pathology)**: Leaf foliage is routed to a 38-class Vision Transformer (`kimcomehome/plantvillage-vit-leaf-disease`) and cross-validated with an EfficientNetB0 backbone. Helianthus (sunflower) queries route to a specialized 4-class classifier (`YaswanthReddy23/ViT_Sunflower`) detecting Gray Mold, Downy Mildew, Leaf Scars, and Healthy Blossoms.
3. **Stage 3 (IP102 Field Pest Localization & Species Classification)**: Multi-pest field images are processed through a YOLO26n 97-class bounding box detector paired with an EfficientNetB0 102-class species classifier trained on the IP102 benchmark.

### Pipeline B — On-Device ExecuTorch Reasoning & Vector RAG
1. **Micro-Quantized Runtime**: Meta's Llama 3.2 1B-Instruct is compiled for ExecuTorch with 4-bit weight quantization (`int4_weight_only`). It executes directly on the four Arm Cortex-A76 cores using Arm KleidiAI and XNNPACK vectorized tensor kernels.
2. **Deterministic Memory Footprint**: The model runtime requires only **1.15 GB of RAM**, leaving 2.85 GB of free physical memory on standard 4GB Raspberry Pi 5 hardware.
3. **ICAR Vector Knowledge Base**: A local ChromaDB SQLite store embeds 122 official ICAR and State Agricultural University (SAU) Package of Practices using `all-MiniLM-L6-v2`. The system grounds every agronomic recommendation in certified scientific research.
4. **Rural Language Relocalization**: The pipeline strips academic jargon (such as "Economic Threshold Level" or "Prophylactic Canopy Closure") and converts recommendations into straightforward, actionable steps with specific fungicide trade names, exact formulations (e.g., *Mancozeb 75% WP @ 2.5 g/L*), water volumes per acre (150–200 L), morning/evening spray windows, and mandatory Pre-Harvest Intervals (PHI).

---

## 4. Methodology & Dataflow Flowcharts

### Flowchart 1: Visual Pathology & Zero-Shot Gatekeeper Pipeline
```mermaid
graph TD
    A["Farmer Image (Mobile Camera / Upload)"] --> B{"SigLIP Gatekeeper<br/>(google/siglip-base-patch16-224)"}
    
    B -->|"Non-Agricultural Subject<br/>(Confidence < 0.40)"| C["HTTP 400 Rejection<br/>Alert: 'No crop foliage or pest detected. Please take a clear photo of the leaf or insect.'"]
    
    B -->|"Crop / Pest Confirmed"| D{"Crop Type & Pest Classifier"}
    
    D -->|"General Crops (Tomato, Potato, Rice, Corn, etc.)"| E["PlantVillage ViT (38 Classes)<br/>+ EfficientNetB0 Dual Check"]
    D -->|"Sunflower (Helianthus)"| F["Sunflower ViT (4 Classes)<br/>Gray Mold, Downy Mildew, Scars, Healthy"]
    D -->|"Field Pest / Insect"| G["YOLO26n + EfficientNetB0 (IP102)<br/>97 Bounding Boxes + 102 Species"]
    
    E --> H["Agronomic Severity Estimator"]
    F --> H
    G --> H
    
    H --> I["Structured Diagnostic Payload:<br/>• Condition Name & Confidence Score<br/>• Severity: None / Mild / Moderate / Critical<br/>• Quality Grade: Grade A / Grade B / Grade C<br/>• Plain-Language Remediation Steps<br/>• Chemical Name, Dosage & Pre-Harvest Interval"]
```

### Flowchart 2: On-Device Vector RAG & Multilingual Advisory Flow
```mermaid
graph TD
    A["Farmer Query (Text or Offline Voice)"] --> B{"Input Mode"}
    B -->|"Voice Audio"| C["Offline Whisper STT"]
    B -->|"Native Text"| D["Text Processor"]
    C --> D
    
    D --> E["Semantic Query Embedding<br/>(all-MiniLM-L6-v2)"]
    
    E --> F[("Local ChromaDB Store<br/>122 Indexed ICAR Packages<br/>Cosine Distance Search")]
    
    F --> G["Retrieved ICAR Agronomic Context"]
    
    G --> H{"ExecuTorch Engine (Arm CPU)<br/>Llama 3.2 1B-Instruct (INT4)<br/>Arm KleidiAI Micro-Kernels"}
    
    H --> I["Agronomic Jargon Purger<br/>Converts ETL & technical metrics to plain steps"]
    
    I --> J["Native-Script Multilingual Synthesis<br/>(English, বাংলা, हिन्दी, etc.)"]
    
    J --> K["Advisory UI Display"]
    J --> L["Offline Text-to-Speech (TTS)"]
    L --> M["Farmer Audio Playback"]
```

### Flowchart 3: Edge Field Station Network Topology
```mermaid
graph LR
    subgraph Offline_Field_Subnet["Local Offline Wi-Fi Hotspot (192.168.5.x)"]
        Phone1["Farmer Smartphone A<br/>(Browser: :8000)"]
        Phone2["Farmer Smartphone B<br/>(Browser: :8000)"]
        Tablet["KVK Extension Tablet<br/>(Browser: :8000)"]
    end

    subgraph Raspberry_Pi_5["Raspberry Pi 5 (Arm Cortex-A76, 4GB RAM)"]
        Router["Hotspot AP / DHCP (192.168.5.200)"]
        FastAPI["FastAPI Edge Server (:8000)<br/>Static React PWA + REST APIs"]
        ExecuTorch["ExecuTorch Llama Microservice (:8008)<br/>INT4 SIMD Quantized"]
        ChromaStore[("ChromaDB SQLite<br/>122 ICAR Chunks")]
        VisionModels["Vision Models Checkpoints<br/>ViT + YOLO + EfficientNet"]
    end

    Phone1 -.->|"Zero Mobile Data"| Router
    Phone2 -.->|"Zero Mobile Data"| Router
    Tablet -.->|"Zero Mobile Data"| Router
    
    Router --> FastAPI
    FastAPI --> ExecuTorch
    FastAPI --> ChromaStore
    FastAPI --> VisionModels
```

---

## 5. Empirical Performance Benchmarks (Raspberry Pi 5)

Evaluated under air-gapped laboratory conditions on a Raspberry Pi 5 (Quad-Core Arm Cortex-A76 @ 2.4 GHz, 4 GB LPDDR4X RAM, active cooler).

| Component / Workload | Model Architecture | Quantization / Format | Latency / Throughput | RAM Utilization | Network Traffic |
|---|---|---|---|---|:---:|
| **Crop Gatekeeper** | SigLIP Base Patch-16 | FP32 (Transformers) | 214 ms | 180 MB | 0.0 KB |
| **Disease Classification** | PlantVillage ViT | FP32 (PyTorch) | 476 ms | 340 MB | 0.0 KB |
| **Sunflower Pathology** | ViT Sunflower | FP32 (PyTorch) | 482 ms | 335 MB | 0.0 KB |
| **Pest Detection** | YOLO26n (97 Classes) | FP32 (PyTorch / Ultralytics) | 312 ms | 210 MB | 0.0 KB |
| **Pest Classification** | EfficientNetB0 (102 Classes) | INT8 / FP32 Keras | 308 ms | 195 MB | 0.0 KB |
| **Vector Retrieval** | all-MiniLM-L6-v2 | ChromaDB SQLite | 18 ms | 120 MB | 0.0 KB |
| **Generative Advisory** | Llama 3.2 1B-Instruct | **INT4 (ExecuTorch / KleidiAI)** | **14.2 tokens/sec** | **1,150 MB** | 0.0 KB |
| **Voice Transcription** | Whisper Tiny | FP32 (ONNX/C++) | 380 ms (5s audio) | 145 MB | 0.0 KB |
| **Full Station Stack** | Combined Pipeline | Multi-Process / Microservices | **117.7 req/s burst** | **2,820 MB / 4,096 MB** | **0.0 KB** |

*Operating Thermals*: Sustained temperature under continuous peak inference loops remained below **58.2°C** with the Raspberry Pi official active cooler.

---

## 6. Core Platform Features

### 1. Visual Crop & Pest Scanner
- Two-stage verification: Rejects non-plant images and identifies specific diseases across tomato, potato, rice, corn, apple, grape, and sunflower.
- Displays diagnostic confidence and disease severity (`Grade A / B / C`, `None`, `Mild`, `Moderate`, `Critical`) side-by-side.
- Provides concrete, safe chemical recommendations with active ingredient concentrations (e.g. *Cymoxanil 8% + Mancozeb 64% WP @ 2.5 g/L* or *Metalaxyl 8% + Mancozeb 64% WP*), exact mixing ratios, and spray schedules.

### 2. Conversational Agronomic Assistant
- Comprehensive coverage across 22 Scheduled Indian Languages plus English, with deep native script localization in Hindi (`हिन्दी`) and Bengali (`বাংলা`).
- Full bidirectional re-localization: Switching languages on the fly instantly updates both the diagnostic advisory and previous chat history without losing context.
- Zero-jargon advisory: Converts academic scientific terminology into clear, numbered actions for smallholder farmers.

### 3. Soil Health Card STCR Fertilizer Calculator
- Implements the Indian Soil Test Crop Response (STCR) 12-parameter agronomic formulation.
- Accepts standard lab readings (pH, Electrical Conductivity, Organic Carbon, Nitrogen, Phosphorus, Potassium, Zinc, Iron, Copper, Manganese, Boron, Sulphur).
- Calculates exact commercial bag counts for Neem-Coated Urea (45 kg bags), DAP (50 kg bags), SSP, MOP, Zinc Sulphate, and Borax.
- Includes mandatory chemical compatibility warnings (e.g., strictly warning against co-applying Zinc Sulphate with DAP/SSP).

### 4. Government Welfare Schemes & Subsidies
- Comprehensive offline knowledge base covering PM-KISAN (direct income support), Kisan Credit Card (concessional credit), and PMFBY (Pradhan Mantri Fasal Bima Yojana).
- Emphasizes critical compliance guidelines, including the mandatory **72-hour crop loss intimation rule** and official national helpline (`14447` and `1800-180-1551`).

### 5. Local Hotspot Field Station
- Built-in Wi-Fi station mode binds to `0.0.0.0:8000`, enabling an entire farming community or KVK extension camp to access the platform via `http://192.168.5.200:8000` through standard mobile phone browsers with zero data connectivity.

---

## 7. Verified Repository Structure

```
ARM/
├── Advisory data/                     # 122 ICAR Package of Practices knowledge base (Markdown)
│   └── india_farmer_advisory_rag_knowledge_base.md
│
├── AgriRakshak_Models_20261118_0437/  # Custom vision checkpoints & taxonomic mappings
│   ├── Disease_Classification/        # EfficientNetB0 disease primary model (.keras)
│   ├── Pest_Classification/           # EfficientNetB0 102-class pest model (.keras)
│   ├── Pest_Detection/                # YOLO26n pest detector weights (best.pt), data.yaml
│   ├── README.txt
│   └── SHA256SUMS.txt                 # Integrity hashes for all model checkpoints
│
├── client/                            # React 19 + TypeScript + Vite offline PWA dashboard
│   ├── src/                           # Multilingual UI components, tabs, audio capture
│   ├── public/                        # Agricultural emblems, offline icons
│   ├── package.json
│   ├── tsconfig.json
│   └── vite.config.ts                 # Configured with base: './' for GitHub Pages compatibility
│
├── docs/                              # Deep-dive architecture notes
│   └── ARM_EXECUTORCH_PIPELINE.md     # ExecuTorch + KleidiAI compilation on Cortex-A76
│
├── llama/                             # ExecuTorch on-device reasoning runtime
│   ├── download_llama.py              # Hugging Face downloader with resume support
│   └── executorch/
│       ├── install_rpi5_arm.sh        # Raspberry Pi 5 system setup script
│       ├── llama_arm_runner.py        # Quantized inference runner with KleidiAI/XNNPACK
│       └── service.py                 # Local microservice (:8008) for FastAPI inter-op
│
├── server/                            # FastAPI offline backend & edge pipelines
│   ├── app/
│   │   ├── main.py                    # API entrypoint, CORS, static SPA mounting
│   │   ├── config.py                  # Strict offline environment settings (HF_HUB_OFFLINE=1)
│   │   ├── rag/                       # ChromaDB vector retriever & prompt synthesizer
│   │   ├── vision/                    # SigLIP gatekeeper, ViT classifiers, YOLO detector
│   │   ├── routers/                   # Health, Vision, Advisory, Soil, Schemes endpoints
│   │   └── schemas/                   # Pydantic v2 schemas for all payloads
│   ├── chroma_db/                     # Local SQLite ChromaDB persistence (122 ICAR vectors)
│   └── run_server.py                  # Standalone backend server entrypoint
│
├── test_eval_suite/                   # 12 test images for pest & disease verification
├── tests/                             # Automated test suites (93 E2E tests + 84 unit tests)
│   ├── e2e_offline_test.py            # Air-gap network isolation & system stress suite
│   ├── e2e_summary.json               # Automated test execution report
│   ├── test_vision.py                 # Vision gatekeeper & classifier regression tests
│   ├── test_rag.py                    # ChromaDB vector retrieval verification
│   ├── test_server.py                 # API router contract tests
│   └── test_multilingual_voice.py     # Language re-localization & translation tests
│
├── .env.example                       # Template environment variables (no secrets)
├── .gitignore                         # Comprehensive multi-runtime ignore specification
├── LICENSE                            # Apache License 2.0
├── README.md                          # Main engineering documentation & architecture specification
├── TECHNICAL_REPORT.md                # Full Arm Bharat AI-SoC challenge technical report
├── TEST_READY.md                      # 93-test automated E2E offline test certification
├── ip102_classes.txt                  # Agricultural pest taxonomic labels (IP102 benchmark)
├── model_benchmark_results.json       # Empirical latency & accuracy logs across models
├── requirements.txt                   # Production Python package dependencies
├── run_server.py                      # Root entrypoint for offline advisory server
├── download_offline_models.py         # Automated Hugging Face / vision weights cache utility
├── evaluate_all_three_models.py       # Triple-backbone comparative evaluation runner
└── start_server.bat                   # Raspberry Pi 5 / Arm64 launch script
```

---

## 8. Quick Start & Setup Guide

### Hardware Prerequisites
- **Target Platform**: Raspberry Pi 5 (4GB or 8GB RAM) or any 64-bit Arm SoC (aarch64).
- **Operating System**: Raspberry Pi OS (64-bit Bookworm/Trixie) or Debian 12/13 ARM64.
- **Python**: Version 3.11 or higher.
- **Node.js**: Version 20 or higher.

### Step 1: Clone Repository & Install Dependencies
```bash
git clone https://github.com/arka05738/krishi-mitra.git
cd krishi-mitra

# Create Python virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install all backend dependencies
pip install -r requirements.txt
```

### Step 2: Cache Offline Models Locally (One-Time Step)
Run the offline caching utility once while internet is connected. After this step, the machine can be completely disconnected from the internet:
```bash
# Cache SigLIP, PlantVillage ViT, Sunflower ViT, and ChromaDB MiniLM
python download_offline_models.py

# Download Llama 3.2 1B-Instruct quantized weights
python llama/download_llama.py
```

### Step 3: Launch Local Services (100% Offline Mode)
Open two terminal windows:

**Terminal 1 (ExecuTorch Llama Reasoning Microservice):**
```bash
python llama/executorch/service.py
# Listening on http://127.0.0.1:8008/generate
```

**Terminal 2 (Krishi Mitra Advisory Server):**
```bash
python run_server.py
# Server binds to 0.0.0.0:8000
# Accessible locally at http://localhost:8000 and via local hotspot at http://192.168.5.200:8000
```

### Step 4: Build or Run Frontend Client
```bash
cd client
npm install
npm run dev
# Or build static production distribution:
npm run build
```

---

## 9. Verification & Automated Testing

The repository includes a comprehensive 93-test automated end-to-end suite that certifies 100% offline air-gapped compliance, boundary resilience, and diagnostic accuracy:

```bash
# 1. Execute Unit & Contract Tests
python -m pytest tests/test_ui_contract.py tests/test_multilingual_voice.py tests/test_vision.py tests/test_server.py tests/test_rag.py -v

# 2. Execute Vision Backbone Benchmark
python evaluate_all_three_models.py

# 3. Execute Complete 93-Test Air-Gapped End-to-End Suite
python tests/e2e_offline_test.py
```

All 93 tests pass with **Exit Code 0** under strict network isolation (`HF_HUB_OFFLINE=1`, `TRANSFORMERS_OFFLINE=1`).

---

## 10. Web Hosting (GitHub Pages)

The client application is automated for static deployment on GitHub Pages.
- **Live URL**: [https://arka05738.github.io/krishi-mitra/](https://arka05738.github.io/krishi-mitra/)

When accessed as a standalone web app, the dashboard operates in interactive preview mode with offline mock data, enabling agricultural officers, evaluators, and researchers to explore the full interface on any desktop or mobile device.

---

## 11. License & Citations

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.

```bibtex
@software{krishi_mitra_2026,
  author = {Arka and Krishi Mitra Development Team},
  title = {Krishi Mitra: 100% Offline AI-SoC Edge Agricultural Advisory System for Arm Platforms},
  year = {2026},
  publisher = {GitHub},
  url = {https://github.com/arka05738/krishi-mitra}
}
```
