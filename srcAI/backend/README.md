# Backend

Professional FastAPI backend for CyberSentinel threat analysis.

## Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py            # FastAPI app & routes
│   ├── models.py          # Pydantic data models
│   ├── config.py          # Environment configuration
│   └── services/
│       ├── __init__.py
│       ├── ollama_client.py   # LLM integration
│       ├── rag.py             # ChromaDB vector retrieval
│       └── pdf_report.py      # PDF generation (fpdf2)
```

## Run

```powershell
# From project root:
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
```

## Env Config

- `ENABLE_CHROMA` – Set to `1` to enable vector DB (default `0`)
- `OLLAMA_URL` – Ollama endpoint (default `http://localhost:11434/api/generate`)
- `MODEL_NAME` – Ollama model name (default `llama3.2`)
- `ALLOWED_ORIGINS` – CORS origins (default includes `localhost:5173`)
- `REPORTS_DIR` – PDF output folder (default `reports`)

## Endpoints

- `GET /` – Service info
- `POST /analyze` – Analyze threat scenario → `ThreatAnalysis`
- `POST /generate-report` – Create PDF from `ThreatAnalysis`
- `GET /health` – System health (Ollama, vector DB status)

## Dependencies

Install via `requirements.txt` in project root:
- fastapi, uvicorn
- requests, pydantic
- sentence-transformers, chromadb
- fpdf2
