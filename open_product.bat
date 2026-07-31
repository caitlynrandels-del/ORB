@echo off
setlocal
set "ROOT=%~dp0"

start "" powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%ROOT%open_product.ps1"

exit /b 0
