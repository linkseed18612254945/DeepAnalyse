#!/usr/bin/env bash
# ─────────────────────────────────────────────────────
#  DIAP — Quick start script for macOS / Linux
# ─────────────────────────────────────────────────────
set -e

echo "[DIAP] Deep Intelligence Analysis Platform — Setup"
echo ""

# ── Backend ──────────────────────────────────────────
pushd backend > /dev/null

if [ ! -f .env ]; then
    echo "[DIAP] Creating backend/.env from .env.example …"
    cp .env.example .env
    echo "[DIAP] Please edit backend/.env with your API keys before running."
fi

if [ ! -d .venv ]; then
    echo "[DIAP] Creating Python virtual environment …"
    python3 -m venv .venv
fi

echo "[DIAP] Activating virtual environment …"
source .venv/bin/activate

echo "[DIAP] Installing Python dependencies …"
pip install -r requirements.txt --quiet

popd > /dev/null

# ── Frontend ─────────────────────────────────────────
pushd frontend > /dev/null

if [ ! -d node_modules ]; then
    echo "[DIAP] Installing frontend dependencies …"
    npm install
fi

popd > /dev/null

echo ""
echo "[DIAP] Setup complete."
echo ""
echo "  Start the backend:"
echo "    cd backend"
echo "    source .venv/bin/activate"
echo "    uvicorn backend.app.main:app --reload"
echo ""
echo "  Start the frontend (in a separate terminal):"
echo "    cd frontend"
echo "    npm run dev"
echo ""
