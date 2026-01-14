import os


# CORS origins (comma-separated)
ALLOWED_ORIGINS = os.getenv(
    "ALLOWED_ORIGINS",
    "http://localhost:5173,http://127.0.0.1:5173,http://localhost:3000,http://localhost:8000,http://127.0.0.1:8000",
).split(",")

# Vector DB toggle
CHROMA_ENABLED = os.getenv("ENABLE_CHROMA", "0") == "1"

# Ollama
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
MODEL_NAME = os.getenv("MODEL_NAME", "llama3.2")

# Files
REPORTS_DIR = os.getenv("REPORTS_DIR", "reports")
