# ─────────────────────────────────────────────────────
#  DIAP — Quick start script for Windows (PowerShell)
# ─────────────────────────────────────────────────────

$ErrorActionPreference = "Stop"

Write-Host "[DIAP] Deep Intelligence Analysis Platform — PowerShell Setup" -ForegroundColor Cyan
Write-Host ""

# ── Backend ──────────────────────────────────────────
Push-Location backend

if (-not (Test-Path .env)) {
    Write-Host "[DIAP] Creating backend\.env from .env.example …"
    Copy-Item .env.example .env
    Write-Host "[DIAP] Please edit backend\.env with your API keys before running." -ForegroundColor Yellow
}

if (-not (Test-Path .venv)) {
    Write-Host "[DIAP] Creating Python virtual environment …"
    python -m venv .venv
}

Write-Host "[DIAP] Activating virtual environment …"
& .venv\Scripts\Activate.ps1

Write-Host "[DIAP] Installing Python dependencies …"
pip install -r requirements.txt --quiet

Pop-Location

# ── Frontend ─────────────────────────────────────────
Push-Location frontend

if (-not (Test-Path node_modules)) {
    Write-Host "[DIAP] Installing frontend dependencies …"
    npm install
}

Pop-Location

Write-Host ""
Write-Host "[DIAP] Setup complete." -ForegroundColor Green
Write-Host ""
Write-Host "  Start the backend:"
Write-Host "    cd backend"
Write-Host "    .venv\Scripts\Activate.ps1"
Write-Host "    uvicorn app.main:app --reload"
Write-Host ""
Write-Host "  Start the frontend (in a separate terminal):"
Write-Host "    cd frontend"
Write-Host "    npm run dev"
Write-Host ""
