#!/usr/bin/env bash
# ==============================================================================
# Bharat AI-SoC Challenge: Arm Education
# Reference Runtime Installation Script for Raspberry Pi 5 (Arm Cortex-A76)
# Target: ExecuTorch + Llama 3.2 1B/3B + XNNPACK/KleidiAI
# ==============================================================================

set -e

echo "=========================================================="
echo " Setting up ExecuTorch on Raspberry Pi 5 (Arm64)"
echo "=========================================================="

# 1. Update system packages
sudo apt update && sudo apt install -y \
    build-essential \
    cmake \
    git \
    python3-dev \
    python3-pip \
    python3-venv \
    libopenblas-dev \
    libatlas-base-dev

# 2. Setup Virtual Environment
if [ ! -d "rpi_venv" ]; then
    python3 -m venv rpi_venv
fi
source rpi_venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install numpy torch torchvision --index-url https://download.pytorch.org/whl/cpu

# 3. Clone and Build ExecuTorch with XNNPACK and Arm KleidiAI
if [ ! -d "executorch" ]; then
    git clone --depth=1 --recurse-submodules https://github.com/pytorch/executorch.git
fi

cd executorch
./install_requirements.sh

# Build ExecuTorch C++ runtime with Arm KleidiAI optimizations
mkdir -p build && cd build
cmake .. \
    -DCMAKE_BUILD_TYPE=Release \
    -DEXECUTORCH_BUILD_XNNPACK=ON \
    -DEXECUTORCH_BUILD_EXTENSION_RUNNER_UTIL=ON \
    -DEXECUTORCH_BUILD_EXTENSION_DATA_LOADER=ON \
    -DEXECUTORCH_BUILD_EXTENSION_MODULE=ON \
    -DEXECUTORCH_BUILD_KERNELS_CUSTOM=ON \
    -DEXECUTORCH_BUILD_KERNELS_OPTIMIZED=ON \
    -DEXECUTORCH_BUILD_SDK=ON

cmake --build . -j$(nproc)

echo "=========================================================="
echo " ExecuTorch Built Successfully for Arm Cortex-A76"
echo " Start Edge Service with: python3 llama_service.py"
echo "=========================================================="
