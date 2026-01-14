import json
import requests
from fastapi import HTTPException
from ..config import OLLAMA_URL, MODEL_NAME


def query_ollama(prompt: str, context: str = "") -> tuple[str, int]:
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
                "options": {"temperature": 0.7, "top_p": 0.9},
            },
            timeout=120,
        )

        if response.status_code == 200:
            result = response.json()
            response_text = result.get("response", "")

            start_idx = response_text.find("{")
            end_idx = response_text.rfind("}") + 1
            if start_idx != -1 and end_idx > start_idx:
                json_str = response_text[start_idx:end_idx]
                token_count = result.get("eval_count", 0) + result.get("prompt_eval_count", 0)
                return json_str, token_count
            return response_text, result.get("eval_count", 0)

        raise Exception(f"Ollama error: {response.status_code}")

    except requests.exceptions.ConnectionError:
        raise HTTPException(
            status_code=503,
            detail="Cannot connect to Ollama. Please ensure Ollama is running on localhost:11434",
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
