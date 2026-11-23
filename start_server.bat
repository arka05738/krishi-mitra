@echo off
title Krishi Mitra - Offline Agricultural Advisory Station
echo =====================================================================
echo   Krishi Mitra -- Offline Agricultural Advisory Station
echo   Mode    : 100%% Offline (Air-Gapped Local Operation)
echo   Hardware: Raspberry Pi 5 (Quad-Core Arm Cortex-A76 @ 2.4GHz)
echo =====================================================================
echo.

:: Enforce 100% Offline Environment Variables
set HF_HUB_OFFLINE=1
set TRANSFORMERS_OFFLINE=1

echo Finding your Wi-Fi Hotspot IP address...
echo Run 'ipconfig' if you need to double-check your Wi-Fi IPv4 address.
echo.
echo Starting Krishi Mitra Advisory Server on port 8000...
echo.
echo   Local Laptop Browser:  http://localhost:8000
echo   Raspberry Pi Browser:  http://^<YOUR_HOTSPOT_IP^>:8000
echo.
echo Press Ctrl+C anytime to stop the server.
echo =====================================================================
echo.

python run_server.py
pause
