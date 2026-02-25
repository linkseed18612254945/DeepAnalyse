"""FastAPI route definitions."""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from fastapi import APIRouter, BackgroundTasks, HTTPException
from sse_starlette.sse import EventSourceResponse

from .pipeline import run_full_pipeline
from .schemas import AnalysisRequest, AnalysisStatusResponse, FollowUpRequest
from ..core.models import AnalysisSession, AnalysisStatus
from ..report.generator import render_markdown

logger = logging.getLogger(__name__)
router = APIRouter()

# In-memory session store (swap for Redis/DB in production)
_sessions: dict[str, AnalysisSession] = {}


# ---------------------------------------------------------------------------
# POST /api/analyse  —  Start a new analysis
# ---------------------------------------------------------------------------

@router.post("/api/analyse", response_model=AnalysisStatusResponse)
async def start_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
) -> AnalysisStatusResponse:
    """Kick off a new intelligence analysis pipeline."""

    session = AnalysisSession(user_input=request.topic)
    _sessions[session.id] = session

    background_tasks.add_task(
        run_full_pipeline, session, request.max_rounds, request.output_formats
    )

    return AnalysisStatusResponse(
        session_id=session.id,
        status=session.status.value,
        progress_messages=["Analysis started"],
    )


# ---------------------------------------------------------------------------
# GET /api/analyse/{session_id}  —  Poll status
# ---------------------------------------------------------------------------

@router.get("/api/analyse/{session_id}", response_model=AnalysisStatusResponse)
async def get_analysis_status(session_id: str) -> AnalysisStatusResponse:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return AnalysisStatusResponse(
        session_id=session.id,
        status=session.status.value,
        progress_messages=session.progress_messages,
        error=session.error,
    )


# ---------------------------------------------------------------------------
# GET /api/analyse/{session_id}/stream  —  SSE progress stream
# ---------------------------------------------------------------------------

@router.get("/api/analyse/{session_id}/stream")
async def stream_progress(session_id: str) -> EventSourceResponse:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    async def event_generator():
        last_index = 0
        while True:
            msgs = session.progress_messages[last_index:]
            for msg in msgs:
                yield {"event": "progress", "data": msg}
            last_index = len(session.progress_messages)

            if session.status in (AnalysisStatus.COMPLETED, AnalysisStatus.FAILED):
                yield {"event": "done", "data": session.status.value}
                break

            await asyncio.sleep(1)

    return EventSourceResponse(event_generator())


# ---------------------------------------------------------------------------
# GET /api/analyse/{session_id}/report  —  Get the final report
# ---------------------------------------------------------------------------

@router.get("/api/analyse/{session_id}/report")
async def get_report(session_id: str) -> dict[str, Any]:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    if session.status != AnalysisStatus.COMPLETED or not session.report:
        raise HTTPException(status_code=409, detail="Report not yet available")

    return {
        "report": session.report.model_dump(),
        "report_markdown": render_markdown(session.report),
    }


# ---------------------------------------------------------------------------
# GET /api/analyse/{session_id}/graph  —  Get the knowledge graph
# ---------------------------------------------------------------------------

@router.get("/api/analyse/{session_id}/graph")
async def get_knowledge_graph(session_id: str) -> dict[str, Any]:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")

    return {
        "entities": [e.model_dump() for e in session.entities],
        "relationships": [r.model_dump() for r in session.relationships],
    }


# ---------------------------------------------------------------------------
# GET /api/analyse/{session_id}/session  —  Full session data
# ---------------------------------------------------------------------------

@router.get("/api/analyse/{session_id}/session")
async def get_full_session(session_id: str) -> dict[str, Any]:
    session = _sessions.get(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    return session.model_dump()


# ---------------------------------------------------------------------------
# GET /api/sessions  —  List all sessions
# ---------------------------------------------------------------------------

@router.get("/api/sessions")
async def list_sessions() -> list[dict[str, Any]]:
    return [
        {
            "id": s.id,
            "user_input": s.user_input[:120],
            "status": s.status.value,
            "created_at": s.created_at.isoformat(),
        }
        for s in _sessions.values()
    ]
