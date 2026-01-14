# 🛡️ CyberSentinel

**AI-Powered Cybersecurity Threat Analysis System**

A locally-runnable, RAG-enhanced threat analysis application that uses open-source LLMs to analyze cybersecurity scenarios and generate detailed reports.

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Python](https://img.shields.io/badge/python-3.11-blue)
![React](https://img.shields.io/badge/react-18.2-blue)

---

## 🎯 Features

- **🤖 AI-Powered Analysis**: Uses local LLMs (Llama 3.2, Mistral, etc.) via Ollama
- **📚 RAG Architecture**: Retrieval-Augmented Generation with ChromaDB vector database
- **🔍 Threat Classification**: Automatically categorizes threats (Phishing, Malware, DDoS, etc.)
- **⚠️ Severity Assessment**: Assigns Low/Medium/High severity levels
- **📋 Mitigation Advice**: Provides actionable security recommendations
- **📄 PDF Reports**: Generate professional threat analysis reports
- **🎨 Modern UI**: Clean, responsive React interface
- **🔒 100% Local**: No cloud APIs, all processing on your machine
- **📊 Token Usage Tracking**: Monitor AI model resource consumption
- **🎯 Interactive Examples**: Quick-start with pre-defined scenarios

---

## 🏗️ Architecture

```
┌─────────────────┐
│  React Frontend │  (Port 3000)
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│  FastAPI Backend│  (Port 8000)
└────────┬────────┘
         │
    ┌────┴────┬────────────┐
    ▼         ▼            ▼
┌────────┐ ┌─────────┐ ┌────────┐
│ChromaDB│ │ Ollama  │ │WeasyPr-│
│ Vector │ │  LLM    │ │  int   │
│   DB   │ │(11434)  │ │  PDF   │
└────────┘ └─────────┘ └────────┘
```

### Components

1. **Frontend (React)**
   - User interface for scenario input
   - Results visualization
   - PDF download functionality

2. **Backend (FastAPI)**
   - REST API endpoints
   - RAG orchestration
   - PDF generation

3. **Vector Database (ChromaDB)**
   - Document embeddings storage
   - Semantic search
   - Context retrieval

4. **LLM (Ollama)**
   - Local model inference
   - Zero cloud dependencies
   - Supports multiple models

---

## 🚀 Quick Start

### Prerequisites

- Docker & Docker Compose
- 8GB+ RAM recommended
- 10GB+ disk space for models

### Installation

1. **Clone/Create the project directory**:
```bash
mkdir cybersentinel && cd cybersentinel
```

2. **Run the automated setup**:
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will:
- Create directory structure
- Install dependencies
- Pull Llama 3.2 model (~2GB)
- Initialize knowledge base
- Start all services

3. **Access the application**:
- Frontend: http://localhost:3000
- API: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📁 Project Structure

```
cybersentinel/
├── backend/
│   ├── main.py                 # FastAPI application
│   ├── ingest_documents.py     # Document ingestion script
│   ├── requirements.txt        # Python dependencies
│   └── Dockerfile             # Backend container
├── frontend/
│   ├── src/
│   │   ├── App.jsx            # Main React component
│   │   ├── App.css            # Styles
│   │   ├── index.js           # Entry point
│   │   └── index.css          # Global styles
│   ├── public/
│   │   └── index.html         # HTML template
│   ├── package.json           # Node dependencies
│   └── Dockerfile             # Frontend container
├── knowledge_base/            # Cybersecurity documents
│   ├── phishing_guide.txt
│   ├── malware_response.txt
│   ├── ddos_mitigation.txt
│   └── insider_threats.txt
├── chroma_db/                 # Vector database storage
├── reports/                   # Generated PDF reports
├── docker-compose.yml         # Container orchestration
├── setup.sh                   # Automated setup script
└── README.md                  # This file
```

---

## 🔧 Manual Setup (Alternative)

If you prefer manual setup:

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt

# Create sample data
python ingest_documents.py

# Run backend
python main.py
```

### 2. Frontend Setup

```bash
cd frontend
npm install
npm start
```

### 3. Ollama Setup

```bash
# Install Ollama from https://ollama.ai
ollama pull llama3.2

# Or use another model:
# ollama pull mistral
# ollama pull openhermes
```

---

## 📖 Usage Guide

### Analyzing a Threat

1. **Enter Scenario**: Describe the cybersecurity incident
2. **Click Analyze**: AI processes with RAG context
3. **Review Results**:
   - Threat type classification
   - Severity level
   - Detailed analysis
   - Mitigation steps
   - Source citations
4. **Download Report**: Generate PDF for documentation

### Example Scenarios

**Phishing Attack**:
```
An employee received an email claiming to be from IT support, 
requesting immediate password verification due to a "security breach."
```

**Malware Infection**:
```
Multiple workstations are experiencing unusual CPU spikes, with 
unknown processes communicating with external IP addresses.
```

**DDoS Attack**:
```
Our web application is receiving 50,000 requests per second from 
various geographic locations, causing service degradation.
```

---

## 🎨 Customization

### Adding Custom Documents

1. **Add files to `knowledge_base/`**:
```bash
cp your_document.pdf knowledge_base/
```

2. **Re-ingest documents**:
```bash
docker-compose run --rm backend python ingest_documents.py
```

Supported formats: PDF, TXT, MD

### Changing the LLM Model

Edit `backend/main.py`:
```python
MODEL_NAME = "mistral"  # or "openhermes", "codellama", etc.
```

Then pull the model:
```bash
docker exec cybersentinel-ollama ollama pull mistral
```

### Adjusting RAG Parameters

In `backend/main.py`, modify:
```python
# Number of context chunks to retrieve
results = collection.query(
    query_texts=[query],
    n_results=5  # Increase for more context
)

# Chunk size during ingestion
chunks = chunk_text(text, chunk_size=1000, overlap=100)
```

---

## 🔍 API Endpoints

### `POST /analyze`
Analyze a threat scenario

**Request**:
```json
{
  "scenario": "Employee clicked suspicious email link..."
}
```

**Response**:
```json
{
  "case_id": "a1b2c3d4",
  "scenario": "Employee clicked suspicious email link...",
  "threat_type": "Phishing",
  "severity": "High",
  "analysis": "This scenario exhibits classic phishing...",
  "recommendations": [
    "Isolate the affected system immediately",
    "Reset user credentials",
    "Scan for malware"
  ],
  "context_sources": ["phishing_guide.txt"],
  "timestamp": "2024-12-11 14:30:00",
  "token_usage": 1250
}
```

### `POST /generate-report`
Generate PDF report (returns PDF file)

### `GET /health`
Check system health

---

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild containers
docker-compose up -d --build

# Access backend shell
docker exec -it cybersentinel-backend bash

# Access Ollama
docker exec -it cybersentinel-ollama bash
```

---

## 🔧 Troubleshooting

### Ollama Connection Issues

**Error**: "Cannot connect to Ollama"

**Solution**:
```bash
# Check Ollama status
docker ps | grep ollama

# Restart Ollama
docker-compose restart ollama

# Verify model is pulled
docker exec cybersentinel-ollama ollama list
```

### ChromaDB Not Found

**Error**: "Collection not found"

**Solution**:
```bash
# Re-ingest documents
docker-compose run --rm backend python ingest_documents.py
```

### Frontend Won't Connect

**Error**: "Network error"

**Solution**:
- Ensure backend is running on port 8000
- Check CORS settings in `main.py`
- Verify `API_BASE` in `App.jsx`

### Model Loading Slow

**Issue**: First query takes 1-2 minutes

**Explanation**: Model loading into memory (normal)

**Solution**: Keep Ollama container running

---

## 📊 Performance Tips

1. **Use Smaller Models**: `llama3.2:1b` for faster responses
2. **Adjust Context**: Reduce `n_results` in RAG queries
3. **GPU Acceleration**: Use Ollama with CUDA support
4. **Increase RAM**: 16GB+ for larger models
5. **SSD Storage**: Faster model loading

---

## 🛡️ Security Considerations

- **Data Privacy**: All processing is local, no data leaves your machine
- **Access Control**: Add authentication to production deployments
- **Network Isolation**: Use Docker networks for security
- **Input Validation**: Sanitize user inputs in production
- **Rate Limiting**: Add API rate limits for public access

---

## 🔄 Updating

### Update Models
```bash
docker exec cybersentinel-ollama ollama pull llama3.2
```

### Update Dependencies
```bash
docker-compose down
docker-compose up -d --build
```

---

## 📝 Sample Output

### Console Output
```
🛡️ Analyzing threat scenario...
✓ Retrieved 3 relevant context chunks
✓ Generated analysis (1,247 tokens)
✓ Classified as: Phishing (High Severity)
✓ Generated 5 mitigation recommendations
✓ PDF report created: reports/cybersentinel_report_a1b2c3d4.pdf
```

### PDF Report Contents
- Case ID and timestamp
- Threat classification
- Severity badge (color-coded)
- Detailed analysis
- Numbered recommendations
- Source citations
- Token usage statistics

---

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Additional threat categories
- More knowledge base documents
- Enhanced UI visualizations
- Support for more document types
- Multi-language support
- Historical analysis tracking

---

## 📄 License

MIT License - feel free to use for any purpose

---

## 🙏 Acknowledgments

- **Ollama**: Local LLM runtime
- **ChromaDB**: Vector database
- **FastAPI**: Modern Python API framework
- **React**: UI library
- **WeasyPrint**: PDF generation
- **Sentence Transformers**: Embeddings

---

## 📞 Support

For issues or questions:
1. Check the troubleshooting section
2. Review Docker logs: `docker-compose logs`
3. Ensure all prerequisites are met
4. Verify Ollama model is downloaded

---

## 🎯 Roadmap

- [ ] Multi-model comparison
- [ ] Historical threat tracking
- [ ] Advanced visualization dashboard
- [ ] Export to multiple formats (DOCX, JSON)
- [ ] Integration with SIEM systems
- [ ] Custom threat playbooks
- [ ] Team collaboration features

---

**Built with ❤️ for the cybersecurity community**

*CyberSentinel - Empowering security professionals with local AI*