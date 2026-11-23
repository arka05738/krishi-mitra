@echo off
title Krishi Mitra - Offline Agricultural Advisory Station
echo =====================================================================
echo   Krishi Mitra -- Offline Agricultural Advisory Station
echo   Mode    : 100%% Offline (Air-Gapped Local Operation)
echo   Hardware: Laptop Server (RTX 3050 GPU) + Raspberry Pi 5 (Edge)
echo =====================================================================
echo.

set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1

cd /d "%~dp0\.."
python run_server.py
pause
