@echo off
REM ─────────────────────────────────────────────────────
REM  DIAP — Quick start script for Windows
REM ─────────────────────────────────────────────────────

echo [DIAP] Deep Intelligence Analysis Platform — Windows Setup
echo.

REM ── Backend ────────────────────────────────────────────
pushd backend

if not exist .env (
    echo [DIAP] Creating backend\.env from .env.example …
    copy .env.example .env >nul
    echo [DIAP] Please edit backend\.env with your API keys before running.
)

if not exist .venv (
    echo [DIAP] Creating Python virtual environment …
    python -m venv .venv
)

echo [DIAP] Activating virtual environment …
call .venv\Scripts\activate.bat

echo [DIAP] Installing Python dependencies …
pip install -r requirements.txt --quiet

popd

REM ── Frontend ───────────────────────────────────────────
pushd frontend

if not exist node_modules (
    echo [DIAP] Installing frontend dependencies …
    call npm install
)

popd

echo.
echo [DIAP] Setup complete.
echo.
echo   Start the backend:
echo     cd backend
echo     .venv\Scripts\activate.bat
echo     uvicorn app.main:app --reload
echo.
echo   Start the frontend (in a separate terminal):
echo     cd frontend
echo     npm run dev
echo.
