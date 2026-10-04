@echo off
title Servidor Kimby QC - Control de Calidad OCR
cd /d "%~dp0"
echo ===================================================
echo   INICIANDO SISTEMA DE CONTROL DE CALIDAD KIMBY
echo ===================================================
echo Abriendo servidor local y navegador...
start http://localhost:8000
python server.py
pause
