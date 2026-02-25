# Deep Intelligence Analysis Platform (DIAP)

AI-driven intelligence analysis platform that goes beyond surface-level information aggregation. Starting from a single trending event or topic, it leverages LLMs and iterative multi-round retrieval to build comprehensive, deeply connected intelligence reports — uncovering hidden relationships, root causes, geopolitical implications, actor motivations, and forward-looking assessments.

## Architecture

```
User Input (Event / Topic)
        │
        ▼
┌───────────────────┐
│  Event Framing    │  ← LLM decomposes into Who/What/When/Where/Why/How/So-What
│  & Scoping Agent  │
└────────┬──────────┘
         │
         ▼
┌───────────────────────────────────────────┐
│         Multi-Round Retrieval Engine      │
│                                           │
│  Round 1: Surface facts & timeline        │
│  Round 2: Key actors & organisations      │
│  Round 3: Historical context & patterns   │
│  Round 4: Hidden connections & networks   │
│  Round 5: Cross-domain connections        │
└────────┬──────────────────────────────────┘
         │
         ▼
┌───────────────────┐
│  Knowledge Graph  │  ← Entities, relationships, confidence scores
│  Builder          │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Analysis &       │  ← Deep synthesis with reasoning chains
│  Synthesis Agent  │
└────────┬──────────┘
         │
         ▼
┌───────────────────┐
│  Report Generator │  ← Structured 10-section intelligence report
└───────────────────┘
```

## Tech Stack

| Layer             | Technology                                    |
|-------------------|-----------------------------------------------|
| LLM Backbone      | Claude (Anthropic) or GPT-4o (OpenAI)        |
| Retrieval          | Tavily / Bing Search API                     |
| Knowledge Graph    | In-memory + optional Neo4j                   |
| Backend            | Python, FastAPI                              |
| Frontend           | React + TypeScript (Vite)                    |
| Report Formats     | Markdown, JSON, PDF, DOCX                    |
| Deployment         | Docker + Docker Compose                      |

## Quick Start

### Prerequisites

- Python 3.12+
- Node.js 20+
- API keys for your chosen LLM and search provider
- Supported platforms: **Windows**, **macOS**, **Linux**

### One-command setup

Cross-platform startup scripts are provided in the `scripts/` directory. They create a virtual environment, install all dependencies, and print next-step instructions.

**macOS / Linux:**

```bash
bash scripts/start.sh
```

**Windows (Command Prompt):**

```cmd
scripts\start.bat
```

**Windows (PowerShell):**

```powershell
.\scripts\start.ps1
```

### Manual setup

#### 1. Backend

```bash
cd backend
```

Copy the env template and fill in your API keys:

| OS | Command |
|----|---------|
| macOS / Linux | `cp .env.example .env` |
| Windows (cmd) | `copy .env.example .env` |
| Windows (PowerShell) | `Copy-Item .env.example .env` |

Create and activate a virtual environment:

| OS | Create venv | Activate |
|----|-------------|----------|
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Windows (cmd) | `python -m venv .venv` | `.venv\Scripts\activate.bat` |
| Windows (PowerShell) | `python -m venv .venv` | `.venv\Scripts\Activate.ps1` |

Install dependencies and start the server:

```bash
pip install -r requirements.txt
uvicorn backend.app.main:app --reload
```

#### 2. Frontend

```bash
cd frontend
npm install
npm run dev
```

#### 3. Docker Compose (Full Stack)

Copy the env template:

| OS | Command |
|----|---------|
| macOS / Linux | `cp backend/.env.example backend/.env` |
| Windows (cmd) | `copy backend\.env.example backend\.env` |
| Windows (PowerShell) | `Copy-Item backend\.env.example backend\.env` |

Edit `backend/.env` with your API keys, then:

```bash
docker compose up --build
```

The frontend will be available at `http://localhost:5173` and the API at `http://localhost:8000`.

### Windows-specific notes

- **WeasyPrint** (PDF generation) requires GTK libraries on Windows. See [WeasyPrint Windows installation](https://doc.courtbouillon.org/weasyprint/stable/first_steps.html#windows). PDF export is optional — Markdown, JSON, and DOCX work without extra dependencies.
- If using **PowerShell** and script execution is restricted, run `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` first.
- All file paths are handled with `pathlib`, so forward-slash and backslash paths both work.

## API Endpoints

| Method | Path                                  | Description                        |
|--------|---------------------------------------|------------------------------------|
| POST   | `/api/analyse`                        | Start a new intelligence analysis  |
| GET    | `/api/analyse/{session_id}`           | Poll analysis status               |
| GET    | `/api/analyse/{session_id}/stream`    | SSE progress stream                |
| GET    | `/api/analyse/{session_id}/report`    | Get the final report               |
| GET    | `/api/analyse/{session_id}/graph`     | Get the knowledge graph            |
| GET    | `/api/analyse/{session_id}/session`   | Get full session data              |
| GET    | `/api/sessions`                       | List all analysis sessions         |
| GET    | `/health`                             | Health check                       |

## Report Sections

The generated intelligence report includes:

1. **Executive Summary** — standalone 2-3 paragraph overview
2. **Event Overview & Context** — timeline, geography, verified facts
3. **Key Actors Analysis** — profiles, roles, relationships, motives
4. **Deep Background** — historical context, structural forces, precedents
5. **Hidden Connections & Network Analysis** — below-the-surface layer
6. **Analytical Assessment** — what it means, why it matters
7. **Scenarios & Implications** — forward-looking with probability weighting
8. **Confidence Assessment** — what is known vs uncertain vs unknown
9. **Key Questions Remaining** — gaps for further investigation
10. **Sources & Citations** — categorised by type and reliability

## Project Structure

```
DeepAnalyse/
├── backend/
│   ├── app/
│   │   ├── agents/
│   │   │   ├── framing_agent.py      # Event decomposition
│   │   │   └── analysis_agent.py     # Deep analysis synthesis
│   │   ├── api/
│   │   │   ├── routes.py             # FastAPI endpoints
│   │   │   ├── pipeline.py           # Orchestration pipeline
│   │   │   └── schemas.py            # Request/response schemas
│   │   ├── core/
│   │   │   ├── config.py             # Settings & env vars
│   │   │   ├── llm.py                # LLM client abstraction
│   │   │   └── models.py             # Domain models
│   │   ├── knowledge/
│   │   │   └── graph.py              # Knowledge graph builder
│   │   ├── report/
│   │   │   └── generator.py          # Report generation & export
│   │   ├── retrieval/
│   │   │   ├── engine.py             # Multi-round retrieval engine
│   │   │   └── search.py             # Web search abstraction
│   │   └── main.py                   # FastAPI app entry-point
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/               # React components
│   │   ├── services/                 # API client
│   │   ├── types/                    # TypeScript types
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── scripts/
│   ├── start.sh                  # macOS / Linux setup
│   ├── start.bat                 # Windows (cmd) setup
│   └── start.ps1                 # Windows (PowerShell) setup
├── docker-compose.yml
├── Dockerfile
└── README.md
```

## License

MIT
