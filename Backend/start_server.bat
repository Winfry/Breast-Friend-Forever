@echo off
echo ========================================
echo Starting Breast Friend Forever Backend
echo ========================================
echo.
echo Server will be accessible at:
echo - Local: http://localhost:8000
echo - Network: http://192.168.1.118:8000
echo.
echo Press Ctrl+C to stop the server
echo ========================================
echo.

cd /d "%~dp0"
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
