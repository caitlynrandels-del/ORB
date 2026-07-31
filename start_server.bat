@echo off
set "ROOT=%~dp0"
set "PY=%ROOT%.venv\Scripts\python.exe"
if exist "%PY%" (
	"%PY%" -m http.server 8000 --directory "%ROOT%ORB"
) else (
	python -m http.server 8000 --directory "%ROOT%ORB"
)
