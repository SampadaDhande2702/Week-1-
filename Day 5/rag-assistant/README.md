## RAG-Lite Document Assistant (Streamlit + FastAPI + FAISS)

### What you get
- **Streamlit UI** (`streamlit_app.py`): upload a PDF and chat
- **FastAPI backend** (`main.py`): `/ingest`, `/chat`, `/health`
- **Vector search**: FAISS (in-memory)
- **Embeddings**: SentenceTransformers (local CPU)
- **LLMs**: Gemini / Groq / Ollama with fallback

### Setup (Windows PowerShell)
From `c:\Users\Dell\Desktop\Myp\rag-assistant`:

```bash
python -m venv venv
.\venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env` and set at least one key:
- `GROQ_API_KEY=...` (recommended)
- or `GEMINI_API_KEY=...`

Optional:
- `OLLAMA_BASE_URL=http://localhost:11434` (default)

### Run (2 terminals)

Terminal 1 (API):

```bash
.\venv\Scripts\activate
uvicorn main:app --host 127.0.0.1 --port 8000
```

Terminal 2 (UI):

```bash
.\venv\Scripts\activate
streamlit run streamlit_app.py
```

Open Streamlit, upload a PDF, then chat.

### Notes
- This is **in-memory** (no persistence). If you refresh the API process, uploaded documents are gone.
- If your primary LLM fails, it falls back automatically (and always tries Ollama last).

