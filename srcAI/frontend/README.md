# Frontend

Static HTML/CSS/JS frontend for CyberSentinel.

## Structure

```
frontend/
├── index.html    # Main UI
└── styles.css    # Styling
```

## Run

```powershell
# From project root:
python -m http.server 5173 --directory frontend
```

Open: http://localhost:5173

## Features

- Health status indicator
- Threat scenario input with example buttons
- Real-time analysis via `/analyze` API
- PDF report download via `/generate-report` API
- Severity badges (Low/Medium/High)
- Recommendations list
- Context sources display

## API Integration

Frontend calls backend on `http://localhost:8000`:
- `GET /health` – Check backend status
- `POST /analyze` – Submit scenario for analysis
- `POST /generate-report` – Download PDF

Ensure backend is running and CORS is configured for `localhost:5173`.
