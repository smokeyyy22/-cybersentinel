# CyberSentinel

**AI-Powered Cybersecurity Threat Analysis System**

A professional, modular application demonstrating:
- **FastAPI backend** with clean service layer (Ollama LLM, optional ChromaDB RAG, PDF reports)
- **Static HTML/CSS frontend** with real-time threat analysis UI
- **Environment-driven config** for flexible deployment
- **Local-first privacy** — no cloud dependencies

---

AI-powered cybersecurity threat analysis with a local LLM backend, optional RAG via ChromaDB, and a minimal web UI.

## Quick Start (Windows)

Prereqs
- Python 3.12 (recommended)
- Ollama (https://ollama.com) with a model pulled (e.g., `llama3.2`)

Setup
```powershell
cd "C:\Users\User\Downloads\salwa AI"
py -3.12 -m venv .\.venv312
.\.venv312\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

Run
```powershell
# Backend (FastAPI)
$env:ENABLE_CHROMA="1"  # optional: enable vector DB
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```
```powershell
# Frontend (static from /frontend)
python -m http.server 5173 --directory frontend
```

Open
- UI: http://localhost:5173
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs
- Health: http://localhost:8000/health

## Environment Variables
- `ENABLE_CHROMA`: `1` to enable ChromaDB (default `0`).
- `OLLAMA_URL`: default `http://localhost:11434/api/generate`.
- `MODEL_NAME`: default `llama3.2`.
- `ALLOWED_ORIGINS`: comma-separated CORS origins, default includes `http://localhost:5173`.

## Ollama
```powershell
ollama serve
ollama pull llama3.2
# optional smaller: ollama pull llama3.2:1b
```

## PDF Generation
- Uses `fpdf2` (pure Python). Downloads to `reports/cybersentinel_report_<CASE>.pdf`.
- If the UI download fails, verify the backend terminal for errors and test directly:
```powershell
$body = '{"case_id":"localtest","scenario":"Test","threat_type":"Phishing","severity":"High","analysis":"Test analysis","recommendations":["Step1"],"context_sources":[],"timestamp":"2025-12-11 12:00:00","token_usage":0}'
curl -Method POST -Uri http://localhost:8000/generate-report -ContentType "application/json" -Body $body -OutFile test.pdf
```

## RAG (Vector DB)
- Local vector DB: ChromaDB with sentence-transformers `all-MiniLM-L6-v2`.
- First run may download the model. If offline, retrieval will return empty context.
- To keep startup fast/offline, set `ENABLE_CHROMA=0`.

## Troubleshooting
- Ports in use:
```powershell
Get-NetTCPConnection -LocalPort 8000 -State Listen
Stop-Process -Id <PID> -Force
Get-NetTCPConnection -LocalPort 5173 -State Listen
Stop-Process -Id <PID> -Force
```
- Ollama busy/blocked:
```powershell
Get-NetTCPConnection -LocalPort 11434 -State Listen | Select OwningProcess
Stop-Process -Id <PID> -Force
ollama serve
```
- CORS: adjust `ALLOWED_ORIGINS` env.

## Project Structure
- `backend/app/main.py` — FastAPI app with routes.
- `backend/app/models.py` — Pydantic models.
- `backend/app/config.py` — Env-driven configuration.
- `backend/app/services/` — `ollama_client.py`, `rag.py`, `pdf_report.py`.
- `frontend/` — `index.html` and `styles.css` static UI.
- `requirements.txt` — Dependencies (FastAPI, ChromaDB, sentence-transformers, fpdf2, etc.).
- `reports/` — Generated PDFs.

## Demo Script (5–7 minutes)
1. Intro (30s): problem (cyber incidents triage) and solution (AI-assisted analysis).
2. Architecture (45s): FastAPI + Ollama + optional Chroma; static UI.
3. Live demo (3–4m):
   - Health: http://localhost:8000/health
   - Analyze a phishing scenario in the UI; explain fields.
   - Download PDF; open the generated file in `reports/`.
4. Design notes (45s):
   - Local-first privacy, configurable model & CORS via env vars.
   - Graceful offline mode (Chroma opt-in, PDF pure-Python).
5. Q&A (30s): performance tips, model swaps, production hardening.

## Report Outline (3–6 pages)
- Abstract: 1 paragraph on goal and result.
- Background: threat analysis workflow, LLM + RAG basics.
- System Design: components, data flow, configuration.
- Implementation: key endpoints (`/analyze`, `/generate-report`), PDF method, Chroma toggle.
- Evaluation: sample scenarios, latency, limitations.
- Future Work: Pinecone/Weaviate, Neo4j graph, auth/rate limits, GPU acceleration.

## Optional Enhancements
- Add ingestion script for Chroma (sample docs) and a toggle in UI to show sources.
- Swap Chroma for Pinecone/Weaviate or add Neo4j if required by curriculum.
- Add `.env` loading (e.g., `python-dotenv`) and production server config.
