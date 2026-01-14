param(
  [switch]$Chroma
)

$env:ENABLE_CHROMA = $(if ($Chroma) { "1" } else { "0" })

if (Test-Path ".\.venv312\Scripts\Activate.ps1") {
  . .\.venv312\Scripts\Activate.ps1
}

python -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000