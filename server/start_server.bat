@echo off
title Krishi Mitra - Offline Agricultural Advisory Station
echo =====================================================================
echo   Krishi Mitra -- Offline Agricultural Advisory Station
echo   Mode    : 100%% Offline (Air-Gapped Local Operation)
echo   Hardware: Raspberry Pi 5 (Quad-Core Arm Cortex-A76 @ 2.4GHz)
echo =====================================================================
echo.

set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1

cd /d "%~dp0\.."
python run_server.py
pause
