# 👗 ANKAN Garments AI Store Manager

An ultra-fast local RAG (Retrieval-Augmented Generation) system for ANKAN Garments.  
Ask questions about your **sales, stock, brands, and trends** in plain English.

---

## ⚡ Why It's Fast
- **Groq LLM** — hardware-accelerated inference (100x faster than local models)
- **FAISS** — millisecond vector similarity search
- **MiniLM embeddings** — tiny but accurate (384-dim)
- **Persistent index** — index once, reload instantly next time

---

## 🚀 How to Run

### Windows
```
Double-click run.bat
```
or in Command Prompt:
```
run.bat
```

### Mac / Linux
```bash
chmod +x run.sh
./run.sh
```

### Manual
```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open **http://localhost:8501** in your browser.

---

## 📁 Adding Your Data

**Option 1 — /data folder (recommended)**
1. Create a `data/` folder in the project directory
2. Drop your CSV or Excel files there (sales, stock, etc.)
3. Check "Auto-load from /data folder" in the sidebar
4. Click **🚀 Process & Index Data**

**Option 2 — Upload via UI**
- Use the file uploader in the sidebar

**Supported formats:** CSV, Excel (.xlsx), PDF, TXT

---

## 💬 Example Questions
- *"Which products have low stock?"*
- *"What is the total revenue this month?"*
- *"Which brands are top sellers?"*
- *"Show me size-wise sales breakdown"*
- *"Which items need to be reordered?"*

---

## ⚙️ Configuration

**Change API Key** — Edit `app.py`, find:
```python
GROQ_API_KEY = "gsk_..."
```
Replace with your key from https://console.groq.com

**Change Model** — Select from the Settings dropdown in the sidebar:
- `llama3-70b-8192` — Most capable (default)
- `llama3-8b-8192` — Fastest
- `mixtral-8x7b-32768` — Good for long context
- `gemma2-9b-it` — Balanced

---

## 📦 Project Structure
```
ankan-garments-rag/
├── app.py                  # Main Streamlit UI
├── requirements.txt        # Python dependencies
├── run.bat                 # Windows launcher
├── run.sh                  # Mac/Linux launcher
├── data/                   # Put your CSV/Excel files here
├── src/
│   ├── llm.py              # Groq LLM handler
│   ├── document_processor.py  # CSV/Excel/PDF parser
│   └── vector_store.py     # FAISS vector index
└── vector_store.pkl        # Auto-saved index (created after first run)
```
