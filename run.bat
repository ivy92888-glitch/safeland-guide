@echo off
title Safeland Guide

REM ====== API Config ======
set LLM_BASE_URL=https://api.siliconflow.cn/v1
set LLM_API_KEY=sk-aaqtcsdmfnrgryqviakmqqqalscwobzduuykpvhgbdskfhkv
set LLM_MODEL=deepseek-ai/DeepSeek-V3

REM ====== Launch ======
cd /d "%~dp0"
echo.
echo ============================================
echo   Safeland Guide - Overseas Survival Assistant
echo   Browser opens http://localhost:8503
echo   Close this window to stop
echo ============================================
echo.

start /b python -m streamlit run chatbot/app.py --server.headless true --server.port 8503
timeout /t 5 /nobreak >nul
start http://localhost:8503

echo Service running. Close this window to stop.
pause
