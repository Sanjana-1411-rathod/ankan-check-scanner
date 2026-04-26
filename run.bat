@echo off
echo ============================================
echo   ANKAN Garments AI RAG System
echo   Powered by Groq + FAISS
echo ============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python not found. Please install Python 3.9+
    pause
    exit /b 1
)

REM Install dependencies
echo [1/2] Installing dependencies...
pip install -r requirements.txt --quiet

echo.
echo [2/2] Starting ANKAN Garments AI...
echo.
echo  Open your browser at: http://localhost:8501
echo  Press Ctrl+C to stop
echo.

streamlit run app.py --server.port 8501 --server.headless false

pause
