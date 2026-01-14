from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from datetime import datetime
import os
# Optional ChromaDB import with graceful fallback
try:
    import chromadb
    from chromadb.utils import embedding_functions
    CHROMA_AVAILABLE = True
except Exception:
    CHROMA_AVAILABLE = False

# Default: keep Chroma off to avoid model downloads when offline.
CHROMA_ENABLED = os.getenv("ENABLE_CHROMA", "0") == "1"
import requests
import json
from pathlib import Path
from fpdf import FPDF
import uuid

app = FastAPI(title="CyberSentinel API")

# Runtime config (env-overridable)
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000",
).split(",")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ChromaDB if available (gracefully skip when offline)
collection = None
if CHROMA_AVAILABLE and CHROMA_ENABLED:
    try:
        chroma_client = chromadb.PersistentClient(path="./chroma_db")
        try:
            embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name="all-MiniLM-L6-v2"
            )
        except Exception as embed_err:
            print(f"Embedding init failed (likely offline): {embed_err}")
            embedding_fn = None

        if embedding_fn:
            try:
                collection = chroma_client.get_collection(
                    name="cybersec_docs",
                    embedding_function=embedding_fn
                )
            except Exception:
                collection = chroma_client.create_collection(
                    name="cybersec_docs",
                    embedding_function=embedding_fn
                )
    except Exception as db_err:
        print(f"Chroma init failed: {db_err}")
        collection = None

# Ollama configuration
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")

class ThreatScenario(BaseModel):
    scenario: str

class ThreatAnalysis(BaseModel):
    case_id: str
    scenario: str
    threat_type: str
    severity: str
    analysis: str
    recommendations: list[str]
    context_sources: list[str]
    timestamp: str
    token_usage: int

def query_ollama(prompt: str, context: str = "") -> tuple[str, int]:
    """Query Ollama local LLM"""
    full_prompt = f"""You are CyberSentinel, an expert cybersecurity threat analyst.

Context from knowledge base:
{context}

User Scenario: {prompt}

Analyze this cybersecurity scenario and provide:
1. Threat Type (e.g., Phishing, Malware, DDoS, Ransomware, Insider Threat, Social Engineering)
2. Severity Level (Low, Medium, or High)
3. Detailed Analysis (2-3 paragraphs)
4. Mitigation Recommendations (specific, actionable steps)

Format your response as JSON:
{{
    "threat_type": "...",
    "severity": "...",
    "analysis": "...",
    "recommendations": ["...", "...", "..."]
}}"""

    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": 0.7,
                    "top_p": 0.9
                }
            },
            timeout=120
        )
        
        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")
            
            # Extract JSON from response
            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                token_count = result.get("eval_count", 0) + result.get("prompt_eval_count", 0)
                return json_str, token_count
            
            return response_text, result.get("eval_count", 0)
        else:
            raise Exception(f"Ollama error: {response.status_code}")
    
    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Please ensure Ollama is running on localhost:11434"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def retrieve_context(query: str, n_results: int = 3) -> tuple[str, list[str]]:
    """Retrieve relevant context from vector DB (fallback to none)."""
    if not collection:
        return "", []
    try:
        results = collection.query(
            query_texts=[query],
            n_results=n_results
        )
        if results["documents"] and results["documents"][0]:
            context = "\n\n".join(results["documents"][0])
            sources = results["metadatas"][0] if results.get("metadatas") else []
            source_names = [s.get("source", "Unknown") for s in sources]
            return context, source_names
        return "", []
    except Exception as e:
        print(f"Context retrieval error: {e}")
        return "", []

def generate_pdf_report(analysis: ThreatAnalysis) -> str:
    """Generate PDF report using fpdf2 (pure Python, no native deps)."""
    try:
        Path("reports").mkdir(exist_ok=True)
        pdf_path = f"reports/cybersentinel_report_{analysis.case_id}.pdf"

        severity_rgb = {
            "Low": (40, 167, 69),
            "Medium": (255, 193, 7),
            "High": (220, 53, 69)
        }
        sev = analysis.severity or "Unknown"
        sev_color = severity_rgb.get(sev, (108, 117, 125))

        pdf = FPDF()
        pdf.add_page()

        pdf.set_font("Helvetica", "B", 18)
        pdf.cell(0, 12, "CyberSentinel Threat Analysis Report", ln=1)
        pdf.set_font("Helvetica", "", 11)
        pdf.cell(0, 8, f"Case ID: {analysis.case_id}", ln=1)
        pdf.cell(0, 8, f"Timestamp: {analysis.timestamp}", ln=1)
        pdf.cell(0, 8, f"Threat Type: {analysis.threat_type}", ln=1)
        pdf.set_text_color(*sev_color)
        pdf.cell(0, 8, f"Severity: {sev}", ln=1)
        pdf.set_text_color(33, 37, 41)
        pdf.cell(0, 8, f"Token Usage: {analysis.token_usage}", ln=1)

        pdf.ln(4)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Scenario", ln=1)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, analysis.scenario)

        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Analysis", ln=1)
        pdf.set_font("Helvetica", "", 11)
        pdf.multi_cell(0, 6, analysis.analysis)

        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Recommendations", ln=1)
        pdf.set_font("Helvetica", "", 11)
        recs = analysis.recommendations or ["No recommendations provided."]
        for idx, rec in enumerate(recs, 1):
            pdf.multi_cell(0, 6, f"{idx}. {rec}")

        pdf.ln(2)
        pdf.set_font("Helvetica", "B", 12)
        pdf.cell(0, 8, "Context Sources", ln=1)
        pdf.set_font("Helvetica", "", 11)
        sources = analysis.context_sources or []
        pdf.multi_cell(0, 6, ", ".join(sources) if sources else "No specific sources cited")

        pdf.output(pdf_path)
        return pdf_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {e}")

@app.get("/")
async def root():
    return {
        "service": "CyberSentinel API",
        "version": "1.0.0",
        "status": "operational"
    }

@app.post("/analyze", response_model=ThreatAnalysis)
async def analyze_threat(scenario: ThreatScenario):
    """Analyze a cybersecurity threat scenario"""
    try:
        # Retrieve context from vector DB
        context, sources = retrieve_context(scenario.scenario)
        
        # Query Ollama with context
        response, token_count = query_ollama(scenario.scenario, context)
        
        # Parse JSON response
        try:
            analysis_data = json.loads(response)
        except json.JSONDecodeError:
            # Fallback parsing
            analysis_data = {
                "threat_type": "Unknown",
                "severity": "Medium",
                "analysis": response,
                "recommendations": ["Review the scenario manually", "Implement standard security protocols"]
            }
        
        # Create analysis object
        analysis = ThreatAnalysis(
            case_id=str(uuid.uuid4())[:8],
            scenario=scenario.scenario,
            threat_type=analysis_data.get("threat_type", "Unknown"),
            severity=analysis_data.get("severity", "Medium"),
            analysis=analysis_data.get("analysis", "Analysis unavailable"),
            recommendations=analysis_data.get("recommendations", []),
            context_sources=sources,
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            token_usage=token_count
        )
        
        return analysis
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/generate-report")
async def generate_report(analysis: ThreatAnalysis):
    """Generate and download PDF report"""
    try:
        pdf_path = generate_pdf_report(analysis)
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"cybersentinel_report_{analysis.case_id}.pdf"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Check system health"""
    try:
        # Check Ollama connection
        ollama_status = "offline"
        try:
            ollama_response = requests.get("http://localhost:11434/api/tags", timeout=5)
            ollama_status = "online" if ollama_response.status_code == 200 else "offline"
        except Exception:
            ollama_status = "offline"

        # Check ChromaDB
        vector_status = "online" if collection else "offline"
        doc_count = 0
        try:
            if collection:
                doc_count = collection.count()
        except Exception:
            vector_status = "degraded"

        return {
            "status": "healthy" if ollama_status == "online" else "degraded",
            "ollama": ollama_status,
            "vector_db": vector_status,
            "documents_indexed": doc_count
        }
    except Exception as e:
        return {
            "status": "degraded",
            "error": str(e)
        }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)