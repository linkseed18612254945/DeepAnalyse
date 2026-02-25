"""API request/response schemas."""

from __future__ import annotations

from pydantic import BaseModel, Field


class AnalysisRequest(BaseModel):
    """Request to start a new intelligence analysis."""
    topic: str = Field(..., min_length=3, description="Event, topic, or URL to analyse")
    max_rounds: int = Field(default=3, ge=1, le=12, description="Maximum retrieval rounds")
    output_formats: list[str] = Field(
        default=["markdown", "json"],
        description="Report output formats: markdown, json, pdf, docx",
    )


class AnalysisStatusResponse(BaseModel):
    session_id: str
    status: str
    progress_messages: list[str] = []
    error: str | None = None


class FollowUpRequest(BaseModel):
    """Ask a follow-up question about an existing analysis."""
    session_id: str
    question: str = Field(..., min_length=3)
