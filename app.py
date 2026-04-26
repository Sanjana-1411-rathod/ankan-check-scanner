import streamlit as st
import os
import tempfile
import time
from document_processor import DocumentProcessor
from vector_store import VectorStore
from llm import LLMHandler

# ─── Page Config ────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ANKAN Garments · AI Store Manager",
    page_icon="👗",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

  /* Hide default streamlit header */
  #MainMenu, footer, header { visibility: hidden; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d0d1a 0%, #111827 100%);
    border-right: 1px solid #1e293b;
  }
  [data-testid="stSidebar"] * { color: #cbd5e1 !important; }

  /* Main background */
  .stApp { background: #0a0f1e; }

  /* Header banner */
  .hero-banner {
    background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%);
    border: 1px solid #312e81;
    border-radius: 16px;
    padding: 28px 36px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
  }
  .hero-banner::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 30% 50%, rgba(99,102,241,0.15) 0%, transparent 60%),
                radial-gradient(circle at 70% 50%, rgba(236,72,153,0.1) 0%, transparent 60%);
  }
  .hero-title {
    font-size: 2rem;
    font-weight: 700;
    color: #f1f5f9;
    margin: 0;
  }
  .hero-subtitle {
    color: #94a3b8;
    font-size: 0.95rem;
    margin-top: 6px;
  }
  .hero-badges span {
    display: inline-block;
    background: rgba(99,102,241,0.2);
    border: 1px solid rgba(99,102,241,0.4);
    color: #a5b4fc;
    border-radius: 20px;
    padding: 3px 12px;
    font-size: 0.75rem;
    margin-right: 8px;
    margin-top: 10px;
  }

  /* Metric cards */
  .metric-card {
    background: linear-gradient(135deg, #111827, #1e293b);
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 18px 20px;
    text-align: center;
    transition: transform 0.2s, border-color 0.2s;
  }
  .metric-card:hover { transform: translateY(-2px); border-color: #6366f1; }
  .metric-value { font-size: 1.6rem; font-weight: 700; color: #f1f5f9; }
  .metric-label { font-size: 0.8rem; color: #64748b; margin-top: 4px; text-transform: uppercase; letter-spacing: 0.5px; }
  .metric-icon { font-size: 1.4rem; margin-bottom: 8px; }

  /* Chat bubbles */
  .chat-user {
    background: linear-gradient(135deg, #4f46e5, #7c3aed);
    color: white;
    border-radius: 18px 18px 4px 18px;
    padding: 14px 18px;
    margin: 10px 0 10px 15%;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(99,102,241,0.3);
  }
  .chat-user-label {
    font-size: 0.72rem;
    color: rgba(255,255,255,0.7);
    margin-bottom: 4px;
    text-align: right;
  }
  .chat-assistant {
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 1px solid #334155;
    color: #e2e8f0;
    border-radius: 4px 18px 18px 18px;
    padding: 14px 18px;
    margin: 10px 15% 10px 0;
    font-size: 0.92rem;
    line-height: 1.6;
    box-shadow: 0 4px 15px rgba(0,0,0,0.3);
    border-left: 3px solid #6366f1;
  }
  .chat-assistant-label {
    font-size: 0.72rem;
    color: #6366f1;
    margin-bottom: 4px;
  }

  /* Quick action buttons */
  div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1e293b, #0f172a) !important;
    border: 1px solid #334155 !important;
    color: #cbd5e1 !important;
    border-radius: 10px !important;
    font-size: 0.82rem !important;
    transition: all 0.2s !important;
    text-align: left !important;
  }
  div[data-testid="stButton"] > button:hover {
    border-color: #6366f1 !important;
    background: linear-gradient(135deg, #1e293b, #1a1f35) !important;
    color: #a5b4fc !important;
    transform: translateX(2px) !important;
  }

  /* Status indicator */
  .status-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    margin-right: 8px;
    animation: pulse 2s infinite;
  }
  .status-ready { background: #22c55e; }
  .status-waiting { background: #f59e0b; }
  @keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.5; }
  }

  /* Chat input */
  [data-testid="stChatInput"] > div {
    background: #1e293b !important;
    border: 1px solid #334155 !important;
    border-radius: 12px !important;
  }
  [data-testid="stChatInput"] textarea {
    color: #f1f5f9 !important;
    background: transparent !important;
  }

  /* Section headers */
  .section-header {
    color: #64748b;
    font-size: 0.72rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    margin: 16px 0 10px;
    padding-bottom: 6px;
    border-bottom: 1px solid #1e293b;
  }

  /* Sidebar file item */
  .file-item {
    background: rgba(99,102,241,0.1);
    border: 1px solid rgba(99,102,241,0.2);
    border-radius: 8px;
    padding: 8px 12px;
    margin: 4px 0;
    font-size: 0.8rem;
    color: #94a3b8;
  }

  /* Groq badge */
  .groq-badge {
    background: linear-gradient(135deg, #f97316, #ea580c);
    color: white;
    border-radius: 6px;
    padding: 2px 8px;
    font-size: 0.7rem;
    font-weight: 600;
  }

  /* Table styling */
  table { color: #e2e8f0 !important; }
  th { color: #a5b4fc !important; border-bottom: 1px solid #334155 !important; }

  /* ── BODY SCANNER BUTTON (new) ── */
  .scanner-btn-wrap {
    margin: 14px 0 4px;
  }
  .scanner-btn {
    display: block;
    width: 100%;
    padding: 13px 16px;
    background: linear-gradient(135deg, #0d9488, #0f766e);
    border: 1px solid #14b8a6;
    border-radius: 12px;
    color: #fff !important;
    font-size: 0.88rem;
    font-weight: 600;
    text-align: center;
    text-decoration: none;
    cursor: pointer;
    letter-spacing: 0.3px;
    box-shadow: 0 0 18px rgba(20,184,166,0.35);
    animation: scanpulse 2.5s ease-in-out infinite;
    transition: box-shadow 0.2s, transform 0.2s;
  }
  .scanner-btn:hover {
    box-shadow: 0 0 30px rgba(20,184,166,0.6);
    transform: translateY(-2px);
    text-decoration: none;
    color: #fff !important;
  }
  @keyframes scanpulse {
    0%, 100% { box-shadow: 0 0 18px rgba(20,184,166,0.35); }
    50%       { box-shadow: 0 0 32px rgba(20,184,166,0.65); }
  }
  .scanner-sub {
    font-size: 0.68rem;
    color: #64748b;
    text-align: center;
    margin-top: 5px;
    letter-spacing: 0.3px;
  }

  /* Body scanner card in action column */
  .scanner-card {
    background: linear-gradient(135deg, #042f2e, #0d3030);
    border: 1px solid #14b8a6;
    border-radius: 12px;
    padding: 16px;
    margin-bottom: 12px;
    text-align: center;
    box-shadow: 0 0 20px rgba(20,184,166,0.2);
    animation: scanpulse 2.5s ease-in-out infinite;
  }
  .scanner-card-icon { font-size: 2rem; margin-bottom: 8px; }
  .scanner-card-title { font-size: 0.9rem; font-weight: 700; color: #5eead4; margin-bottom: 4px; }
  .scanner-card-sub { font-size: 0.75rem; color: #94a3b8; margin-bottom: 12px; line-height: 1.5; }
  .scanner-card a {
    display: inline-block;
    padding: 9px 20px;
    background: linear-gradient(135deg, #0d9488, #0f766e);
    border: 1px solid #14b8a6;
    border-radius: 8px;
    color: #fff !important;
    font-size: 0.82rem;
    font-weight: 600;
    text-decoration: none;
    letter-spacing: 0.3px;
  }
  .scanner-card a:hover { opacity: 0.88; text-decoration: none; color: #fff !important; }
</style>
""", unsafe_allow_html=True)

# ─── Session State ───────────────────────────────────────────────────────────
for key, default in {
    "chat_history": [],
    "vector_store": None,
    "processed": False,
    "total_chunks": 0,
    "files_loaded": [],
}.items():
    if key not in st.session_state:
        st.session_state[key] = default

# ─── Config ──────────────────────────────────────────────────────────────────
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")
VECTOR_STORE_PATH = "vector_store.pkl"
BODY_SCANNER_URL = "https://elegant-semolina-ed569e.netlify.app/"

# ─── Sidebar ─────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 12px 0 20px;'>
      <div style='font-size:2rem;'>👗</div>
      <div style='font-size:1rem; font-weight:700; color:#f1f5f9;'>ANKAN Garments</div>
      <div style='font-size:0.72rem; color:#64748b; margin-top:4px;'>AI Store Intelligence</div>
      <div style='margin-top:10px;'><span class='groq-badge'>⚡ GROQ POWERED</span></div>
    </div>
    """, unsafe_allow_html=True)

    # ── BODY SCANNER BUTTON IN SIDEBAR (new) ────────────────────────────────
    st.markdown(f"""
    <div class="scanner-btn-wrap">
      <a class="scanner-btn" href="{BODY_SCANNER_URL}" target="_blank">
        🫁 &nbsp; Body Scanner
      </a>
      <div class="scanner-sub">AI Body Measurement App ↗</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-header">📁 Data Upload</div>', unsafe_allow_html=True)

    uploaded_files = st.file_uploader(
        "CSV / Excel / PDF / TXT",
        type=["csv", "xlsx", "pdf", "txt"],
        accept_multiple_files=True,
        label_visibility="collapsed"
    )

    auto_load = st.checkbox("Auto-load /data folder", value=True)

    if st.button("🚀 Process & Index Data", use_container_width=True):
        all_files = []

        if uploaded_files:
            tmp_dir = tempfile.gettempdir()
            for uf in uploaded_files:
                path = os.path.join(tmp_dir, uf.name)
                with open(path, "wb") as f:
                    f.write(uf.getbuffer())
                all_files.append(path)

        if auto_load and os.path.exists("data"):
            for fname in os.listdir("data"):
                fpath = os.path.join("data", fname)
                if os.path.isfile(fpath):
                    all_files.append(fpath)

        if not all_files:
            st.error("No files found!")
        else:
            progress = st.progress(0, "Initializing...")
            processor = DocumentProcessor()
            all_chunks = []
            names = []

            for i, fpath in enumerate(all_files):
                progress.progress((i + 1) / (len(all_files) + 1), f"Reading {os.path.basename(fpath)}...")
                chunks = processor.process_file(fpath)
                all_chunks.extend(chunks)
                names.append(f"{os.path.basename(fpath)} ({len(chunks)} chunks)")

            progress.progress(0.85, "Building vector index...")
            vs = VectorStore()
            vs.add_documents(all_chunks)
            vs.save(VECTOR_STORE_PATH)

            st.session_state.vector_store = vs
            st.session_state.processed = True
            st.session_state.total_chunks = len(all_chunks)
            st.session_state.files_loaded = names

            progress.progress(1.0, "Done!")
            time.sleep(0.5)
            progress.empty()
            st.success(f"✅ Indexed {len(all_chunks)} chunks!")

    # Load existing index
    if not st.session_state.processed and os.path.exists(VECTOR_STORE_PATH):
        if st.button("📂 Load Saved Index", use_container_width=True):
            with st.spinner("Loading index..."):
                vs = VectorStore()
                vs.load(VECTOR_STORE_PATH)
                st.session_state.vector_store = vs
                st.session_state.processed = True
                st.session_state.total_chunks = len(vs.documents)
                st.success("✅ Saved index loaded!")

    # Show loaded files
    if st.session_state.files_loaded:
        st.markdown('<div class="section-header">📄 Loaded Files</div>', unsafe_allow_html=True)
        for fname in st.session_state.files_loaded:
            st.markdown(f'<div class="file-item">📄 {fname}</div>', unsafe_allow_html=True)

    st.markdown('<div class="section-header">⚙️ Settings</div>', unsafe_allow_html=True)
    top_k = st.slider("Context depth (Top K)", 1, 10, 5)
    model_choice = st.selectbox("Groq Model", [
        "llama-3.3-70b-versatile",
        "llama-3.1-8b-instant",
        "gemma2-9b-it",
        "llama3-8b-8192",
    ], index=0)

    st.markdown('<div class="section-header">🗑️ Actions</div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("Clear Chat", use_container_width=True):
            st.session_state.chat_history = []
            st.rerun()
    with col_b:
        if st.button("Reset All", use_container_width=True):
            for k in ["chat_history", "vector_store", "processed", "total_chunks", "files_loaded"]:
                st.session_state[k] = [] if k in ["chat_history", "files_loaded"] else (None if k == "vector_store" else False if k == "processed" else 0)
            st.rerun()

# ─── Hero Banner ─────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero-banner">
  <h1 class="hero-title">👗 ANKAN Garments · AI Store Manager</h1>
  <p class="hero-subtitle">Ask anything about your sales, stock, brands & trends — powered by Groq AI</p>
  <div class="hero-badges">
    <span>⚡ Ultra-fast Groq LLM</span>
    <span>🔍 FAISS Vector Search</span>
    <span>📊 Sales Analytics</span>
    <span>📦 Stock Alerts</span>
  </div>
</div>
""", unsafe_allow_html=True)

# ─── Status + Metrics Row ────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

status_html = (
    '<span class="status-dot status-ready"></span> Ready'
    if st.session_state.processed
    else '<span class="status-dot status-waiting"></span> Awaiting Data'
)

with c1:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">🟢</div>
      <div class="metric-value" style='font-size:1rem;'>{status_html}</div>
      <div class="metric-label">System Status</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">🧩</div>
      <div class="metric-value">{st.session_state.total_chunks:,}</div>
      <div class="metric-label">Indexed Chunks</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">💬</div>
      <div class="metric-value">{len(st.session_state.chat_history) // 2}</div>
      <div class="metric-label">Questions Asked</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown(f"""
    <div class="metric-card">
      <div class="metric-icon">⚡</div>
      <div class="metric-value" style='font-size:0.95rem;'>{model_choice.split('-')[0].upper()}</div>
      <div class="metric-label">Active Model</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─── Main Content: Chat + Quick Actions ──────────────────────────────────────
chat_col, action_col = st.columns([3, 1])

with action_col:
    st.markdown("""
    <div style='background: linear-gradient(135deg,#111827,#1e293b); border:1px solid #1e293b;
    border-radius:12px; padding:16px; margin-bottom:12px;'>
      <div style='color:#6366f1; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px;'>
        ⚡ Quick Insights
      </div>
    """, unsafe_allow_html=True)

    quick = {
        "📦 Low Stock Alert":    "Which products have low stock or are about to run out?",
        "🏆 Top Selling Items":  "What are the top 10 best selling products and brands?",
        "💰 Revenue Summary":    "Give me a complete summary of total revenue and sales performance.",
        "📊 Size Trends":        "Which sizes and categories are performing the best?",
        "🏷️ Brand Analysis":    "Which brands are selling the most and which are slow movers?",
        "📈 Recent Sales":       "What are the recent sales trends? Show me month-wise or date-wise if available.",
        "🔄 Reorder Needed":     "Which items need to be reordered based on stock levels?",
    }

    for label, question in quick.items():
        if st.button(label, use_container_width=True, key=f"qbtn_{label}"):
            if st.session_state.processed:
                st.session_state.chat_history.append({"role": "user", "content": question})
                st.rerun()
            else:
                st.warning("Process data first!")

    st.markdown("</div>", unsafe_allow_html=True)

    # Tips card
    st.markdown("""
    <div style='background:rgba(99,102,241,0.08); border:1px solid rgba(99,102,241,0.2);
    border-radius:12px; padding:14px; margin-top:8px;'>
      <div style='color:#6366f1; font-size:0.72rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:8px;'>
        💡 Tips
      </div>
      <div style='color:#64748b; font-size:0.78rem; line-height:1.6;'>
        • Upload CSV/Excel from the sidebar<br>
        • Ask about specific brands or SKUs<br>
        • Ask for date-wise or month-wise trends<br>
        • Compare categories side by side
      </div>
    </div>
    """, unsafe_allow_html=True)

with chat_col:
    # Chat history
    chat_container = st.container()
    with chat_container:
        if not st.session_state.chat_history:
            st.markdown("""
            <div style='text-align:center; padding:60px 20px; color:#334155;'>
              <div style='font-size:3rem; margin-bottom:16px;'>💬</div>
              <div style='font-size:1.1rem; color:#475569; margin-bottom:8px;'>Start a conversation</div>
              <div style='font-size:0.85rem; color:#334155;'>
                Upload your sales & stock data, then ask anything!<br>
                Use the Quick Insights buttons on the right →
              </div>
            </div>
            """, unsafe_allow_html=True)
        else:
            for msg in st.session_state.chat_history:
                if msg["role"] == "user":
                    st.markdown(f"""
                    <div class='chat-user-label'>You</div>
                    <div class='chat-user'>{msg['content']}</div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                    <div class='chat-assistant-label'>⚡ ANKAN AI</div>
                    <div class='chat-assistant'>{msg['content']}</div>
                    """, unsafe_allow_html=True)

    # Chat input
    user_input = st.chat_input("Ask about sales, stock, brands, sizes...")

    # Handle quick button trigger (odd history = unanswered question)
    pending = None
    if user_input:
        pending = user_input
    elif (
        st.session_state.chat_history
        and len(st.session_state.chat_history) % 2 != 0
    ):
        pending = st.session_state.chat_history[-1]["content"]

    if pending and st.session_state.processed:
        # Avoid duplicate push
        if not st.session_state.chat_history or st.session_state.chat_history[-1]["content"] != pending:
            st.session_state.chat_history.append({"role": "user", "content": pending})

        with st.spinner("⚡ Thinking with Groq..."):
            t0 = time.time()
            results = st.session_state.vector_store.search(pending, top_k=top_k)
            context = "\n\n".join(results)
            llm = LLMHandler(api_key=GROQ_API_KEY, model_name=model_choice)
            answer = llm.get_answer(query=pending, context=context)
            elapsed = time.time() - t0

            # Append timing to answer
            answer += f"\n\n---\n*⚡ Answered in {elapsed:.1f}s using {model_choice}*"
            st.session_state.chat_history.append({"role": "assistant", "content": answer})
            st.rerun()

    elif pending and not st.session_state.processed:
        st.error("⚠️ Please upload data and click **Process & Index Data** first!")
