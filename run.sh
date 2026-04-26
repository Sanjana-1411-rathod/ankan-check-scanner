#!/bin/bash
echo "============================================"
echo "  ANKAN Garments AI RAG System"
echo "  Powered by Groq + FAISS"
echo "============================================"
echo ""

# Install dependencies
echo "[1/2] Installing dependencies..."
pip install -r requirements.txt -q

echo ""
echo "[2/2] Starting ANKAN Garments AI..."
echo ""
echo "  Open your browser at: http://localhost:8501"
echo "  Press Ctrl+C to stop"
echo ""

streamlit run app.py --server.port 8501
