@echo off
echo Starting FastAPI Backend Server (Production Mode - All Networks)...
echo This allows connection from Android Emulator and Physical Devices
echo.
cd /d %~dp0
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000
pause
