@echo off
set "ROOT=%~dp0"
"%ROOT%.venv\Scripts\python.exe" -m http.server 8000 --directory "%ROOT%ORB"
