# 🚀 CyberSentinel - Complete Deployment Guide

This guide will walk you through setting up CyberSentinel from scratch on any system.

---

## 📋 Table of Contents

1. [System Requirements](#system-requirements)
2. [Installation Methods](#installation-methods)
3. [Step-by-Step Setup](#step-by-step-setup)
4. [Testing the Application](#testing-the-application)
5. [Production Deployment](#production-deployment)
6. [Troubleshooting](#troubleshooting)

---

## 💻 System Requirements

### Minimum Requirements
- **OS**: Linux, macOS, or Windows (with WSL2)
- **RAM**: 8GB (16GB recommended)
- **Storage**: 15GB free space
- **CPU**: 4 cores (8 cores recommended)
- **Docker**: 20.10 or higher
- **Docker Compose**: 2.0 or higher

### Recommended Requirements
- **RAM**: 16GB+
- **Storage**: SSD with 20GB+ free
- **CPU**: 8+ cores
- **GPU**: NVIDIA GPU (optional, for faster inference)

---

## 🎯 Installation Methods

Choose one of the following methods:

### Method 1: Automated Setup (Recommended)
Use the provided `setup.sh` script - fastest and easiest.

### Method 2: Docker Compose
Manual Docker setup - good for customization.

### Method 3: Local Development
Run components individually - best for development.

---

## 📦 Method 1: Automated Setup

### Step 1: Create Project Directory

```bash
# Create main directory
mkdir cybersentinel
cd cybersentinel

# Create subdirectories
mkdir -p backend frontend knowledge_base chroma_db reports
```

### Step 2: Download Setup Script

Create `setup.sh` with the provided content, then:

```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Wait for Setup

The script will:
1. ✅ Verify Docker installation
2. ✅ Create directory structure
3. ✅ Build Docker containers
4. ✅ Pull Llama 3.2 model (~2GB download)
5. ✅ Initialize knowledge base
6. ✅ Start all services

**Expected time**: 10-20 minutes (depending on internet speed)

### Step 4: Verify Installation

```bash
# Check all containers are running
docker ps

# You should see:
# - cybersentinel-backend
# - cybersentinel-frontend  
# - cybersentinel-ollama
```

### Step 5: Access Application

Open your browser to: **http://localhost:3000**

---

## 🔧 Method 2: Manual Docker Compose Setup

### Step 1: Create Files

Create all the following files in their respective directories:

#### 1. `docker-compose.yml` (root)
```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: cybersentinel-backend
    ports:
      - "8000:8000"
    volumes:
      - ./backend:/app
      - ./chroma_db:/app/chroma_db
      - ./reports:/app/reports
      - ./knowledge_base:/app/knowledge_base
    environment:
      - PYTHONUNBUFFERED=1
    network_mode: host
    restart: unless-stopped

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: cybersentinel-frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
      - /app/node_modules
    stdin_open: true
    tty: true
    restart: unless-stopped

  ollama:
    image: ollama/ollama:latest
    container_name: cybersentinel-ollama
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    restart: unless-stopped

volumes:
  ollama_data:
    driver: local
```

#### 2. `backend/Dockerfile`
```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    libcairo2 \
    libpangocairo-1.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/chroma_db /app/reports /app/knowledge_base

EXPOSE 8000
CMD ["python", "main.py"]
```

#### 3. `backend/requirements.txt`
```
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
chromadb==0.4.22
sentence-transformers==2.3.1
requests==2.31.0
weasyprint==60.2
PyPDF2==3.0.1
python-multipart==0.0.6
```

#### 4. `backend/main.py`
Copy the complete backend code from the first artifact.

#### 5. `backend/ingest_documents.py`
Copy the ingestion script from the second artifact.

#### 6. `frontend/Dockerfile`
```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .
EXPOSE 3000
CMD ["npm", "start"]
```

#### 7. `frontend/package.json`
```json
{
  "name": "cybersentinel-frontend",
  "version": "1.0.0",
  "private": true,
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-scripts": "5.0.1"
  },
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build"
  }
}
```

#### 8. `frontend/public/index.html`
```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>CyberSentinel</title>
  </head>
  <body>
    <div id="root"></div>
  </body>
</html>
```

#### 9. `frontend/src/index.js`
```javascript
import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(<React.StrictMode><App /></React.StrictMode>);
```

#### 10. `frontend/src/index.css`
```css
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
}
```

#### 11. `frontend/src/App.jsx`
Copy the React component from the third artifact.

#### 12. `frontend/src/App.css`
Copy the CSS from the fourth artifact.

### Step 2: Build and Start

```bash
# Start Ollama first
docker-compose up -d ollama

# Wait for Ollama to be ready (30 seconds)
sleep 30

# Pull the model
docker exec cybersentinel-ollama ollama pull llama3.2

# Initialize knowledge base
docker-compose build backend
docker-compose run --rm backend python ingest_documents.py

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f
```

---

## 💻 Method 3: Local Development Setup

### Backend Setup

```bash
cd backend

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Create sample data and ingest
python ingest_documents.py

# Run backend
python main.py
```

Backend will run on: **http://localhost:8000**

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm start
```

Frontend will run on: **http://localhost:3000**

### Ollama Setup

```bash
# Install Ollama from https://ollama.ai
# Then pull model:
ollama pull llama3.2

# Verify it's running:
curl http://localhost:11434/api/tags
```

---

## 🧪 Testing the Application

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "ollama": "online",
  "vector_db": "online",
  "documents_indexed": 48
}
```

### 2. Test Analysis

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"scenario": "Employee received suspicious email with attachment"}'
```

### 3. Test Frontend

1. Open http://localhost:3000
2. Click an example scenario
3. Click "Analyze Threat"
4. Wait for results (30-60 seconds)
5. Click "Download PDF Report"

### 4. Verify PDF Generation

Check the `reports/` directory:
```bash
ls -lh reports/
```

You should see generated PDF files.

---

## 🏭 Production Deployment

### 1. Environment Variables

Create `.env` file:
```bash
# Backend
BACKEND_PORT=8000
MODEL_NAME=llama3.2
OLLAMA_URL=http://ollama:11434

# Frontend  
REACT_APP_API_URL=http://your-domain.com/api

# Security
ALLOWED_ORIGINS=https://your-domain.com
```

### 2. Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 3. SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### 4. Systemd Service

Create `/etc/systemd/system/cybersentinel.service`:
```ini
[Unit]
Description=CyberSentinel
After=docker.service
Requires=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/path/to/cybersentinel
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable cybersentinel
sudo systemctl start cybersentinel
```

---

## 🐛 Troubleshooting

### Issue: Docker containers won't start

**Solution**:
```bash
# Check logs
docker-compose logs

# Rebuild containers
docker-compose down
docker-compose up -d --build
```

### Issue: Ollama model not found

**Solution**:
```bash
# List available models
docker exec cybersentinel-ollama ollama list

# Pull model again
docker exec cybersentinel-ollama ollama pull llama3.2
```

### Issue: Backend can't connect to Ollama

**Solution**:
```bash
# Verify Ollama is running
curl http://localhost:11434/api/tags

# Check network mode in docker-compose.yml
# Should be: network_mode: host
```

### Issue: ChromaDB empty or not found

**Solution**:
```bash
# Re-ingest documents
docker-compose run --rm backend python ingest_documents.py

# Check vector count
docker-compose exec backend python -c "
import chromadb
client = chromadb.PersistentClient(path='./chroma_db')
col = client.get_collection('cybersec_docs')
print(f'Documents: {col.count()}')
"
```

### Issue: Frontend shows connection error

**Solution**:
```bash
# Verify backend is running
curl http://localhost:8000/health

# Check CORS settings in backend/main.py
# Verify API_BASE in frontend/src/App.jsx
```

### Issue: PDF generation fails

**Solution**:
```bash
# Install system dependencies
docker-compose exec backend apt-get update
docker-compose exec backend apt-get install -y \
    libpango-1.0-0 libcairo2 libgdk-pixbuf2.0-0
```

### Issue: Out of memory

**Solution**:
- Use a smaller model: `llama3.2:1b`
- Reduce batch size in embeddings
- Increase Docker memory limit
- Add swap space

---

## 📊 Performance Optimization

### 1. Use Quantized Models

```bash
# 4-bit quantized (faster, less memory)
docker exec cybersentinel-ollama ollama pull llama3.2:q4_0
```

Update `backend/main.py`:
```python
MODEL_NAME = "llama3.2:q4_0"
```

### 2. GPU Acceleration

Install NVIDIA Container Toolkit:
```bash
distribution=$(. /etc/os-release;echo $ID$VERSION_ID)
curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add -
curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | \
    sudo tee /etc/apt/sources.list.d/nvidia-docker.list

sudo apt-get update && sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker
```

Update `docker-compose.yml`:
```yaml
ollama:
  image: ollama/ollama:latest
  runtime: nvidia
  environment:
    - NVIDIA_VISIBLE_DEVICES=all
```

### 3. Optimize ChromaDB

```python
# In backend/main.py
collection = chroma_client.create_collection(
    name="cybersec_docs",
    embedding_function=embedding_fn,
    metadata={"hnsw:space": "cosine"}  # Faster similarity search
)
```

---

## 🔄 Updating the Application

### Update Docker Images

```bash
docker-compose pull
docker-compose up -d --build
```

### Update Ollama Model

```bash
docker exec cybersentinel-ollama ollama pull llama3.2
docker-compose restart backend
```

### Update Knowledge Base

```bash
# Add new documents to knowledge_base/
docker-compose run --rm backend python ingest_documents.py
```

---

## 📈 Monitoring

### View Logs

```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend

# Last 100 lines
docker-compose logs --tail=100
```

### Resource Usage

```bash
docker stats cybersentinel-backend cybersentinel-frontend cybersentinel-ollama
```

### Health Monitoring Script

Create `monitor.sh`:
```bash
#!/bin/bash
while true; do
    echo "=== Health Check ===" 
    curl -s http://localhost:8000/health | jq
    echo ""
    sleep 60
done
```

---

## 🎓 Next Steps

1. ✅ Add your own cybersecurity documents
2. ✅ Customize the UI theme
3. ✅ Integrate with your SIEM
4. ✅ Set up automated backups
5. ✅ Create custom threat playbooks
6. ✅ Deploy to production with SSL

---

## 📚 Additional Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [ChromaDB Documentation](https://docs.trychroma.com/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)

---

## 🎉 Congratulations!

You now have a fully functional AI-powered cybersecurity threat analysis system running locally!

**Happy threat hunting! 🛡️**