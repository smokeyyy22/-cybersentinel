from datetime import datetime
import json
import uuid

import requests
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from .config import ALLOWED_ORIGINS
from .models import ThreatScenario, ThreatAnalysis
from .services.ollama_client import query_ollama
from .services.pdf_report import generate_pdf_report
from .services.rag import retrieve_context, vector_status


app = FastAPI(title="CyberSentinel API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/api/")
async def root():
    return {"service": "CyberSentinel API", "version": "1.0.0", "status": "operational"}


@app.post("/api/analyze", response_model=ThreatAnalysis)
async def analyze_threat(scenario: ThreatScenario):
    try:
        context, sources = retrieve_context(scenario.scenario)
        response, token_count = query_ollama(scenario.scenario, context)

        try:
            analysis_data = json.loads(response)
        except json.JSONDecodeError:
            analysis_data = {
                "threat_type": "Unknown",
                "severity": "Medium",
                "analysis": response,
                "recommendations": [
                    "Review the scenario manually",
                    "Implement standard security protocols",
                ],
            }

        analysis = ThreatAnalysis(
            case_id=str(uuid.uuid4())[:8],
            scenario=scenario.scenario,
            threat_type=analysis_data.get("threat_type", "Unknown"),
            severity=analysis_data.get("severity", "Medium"),
            analysis=analysis_data.get("analysis", "Analysis unavailable"),
            recommendations=analysis_data.get("recommendations", []),
            context_sources=sources,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            token_usage=token_count,
        )

        return analysis
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/generate-report")
async def generate_report(analysis: ThreatAnalysis):
    try:
        pdf_path = generate_pdf_report(analysis)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"cybersentinel_report_{analysis.case_id}.pdf",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/health")
async def health_check():
    try:
        ollama_status = "offline"
        try:
            resp = requests.get("http://localhost:11434/api/tags", timeout=5)
            ollama_status = "online" if resp.status_code == 200 else "offline"
        except Exception:
            ollama_status = "offline"

        vector_db_status, doc_count = vector_status()

        return {
            "status": "healthy" if ollama_status == "online" else "degraded",
            "ollama": ollama_status,
            "vector_db": vector_db_status,
            "documents_indexed": doc_count,
        }
    except Exception as e:
        return {"status": "degraded", "error": str(e)}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
