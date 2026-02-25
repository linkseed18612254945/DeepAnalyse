"""Domain models shared across the application."""

from __future__ import annotations

import uuid
from datetime import datetime
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


# ---------------------------------------------------------------------------
# Enums
# ---------------------------------------------------------------------------

class ConfidenceLevel(str, Enum):
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"
    SPECULATIVE = "speculative"


class SourceTier(int, Enum):
    OFFICIAL = 1        # Official records, wire services
    ESTABLISHED = 2     # Established media
    SECONDARY = 3       # Secondary sources
    UNVERIFIED = 4      # Social media / unverified


class AnalysisStatus(str, Enum):
    PENDING = "pending"
    FRAMING = "framing"
    RETRIEVING = "retrieving"
    EXTRACTING = "extracting"
    ANALYZING = "analyzing"
    GENERATING_REPORT = "generating_report"
    COMPLETED = "completed"
    FAILED = "failed"


class RelationshipType(str, Enum):
    OWNS = "owns"
    CONTROLS = "controls"
    FUNDS = "funds"
    OPPOSES = "opposes"
    INFLUENCES = "influences"
    ALLIED_WITH = "allied_with"
    MEMBER_OF = "member_of"
    SUBSIDIARY_OF = "subsidiary_of"
    LOCATED_IN = "located_in"
    PARTICIPATED_IN = "participated_in"
    RELATED_TO = "related_to"


# ---------------------------------------------------------------------------
# Source & Citation
# ---------------------------------------------------------------------------

class Source(BaseModel):
    url: str = ""
    title: str = ""
    domain: str = ""
    tier: SourceTier = SourceTier.UNVERIFIED
    snippet: str = ""
    retrieved_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Entities & Relationships (Knowledge Graph)
# ---------------------------------------------------------------------------

class Entity(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    name: str
    entity_type: str  # person, organization, location, event, legislation, etc.
    description: str = ""
    attributes: dict[str, Any] = Field(default_factory=dict)
    sources: list[Source] = Field(default_factory=list)


class Relationship(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:12])
    source_entity_id: str
    target_entity_id: str
    relationship_type: RelationshipType = RelationshipType.RELATED_TO
    description: str = ""
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    sources: list[Source] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Retrieval Round
# ---------------------------------------------------------------------------

class RetrievalQuery(BaseModel):
    query: str
    rationale: str = ""


class RetrievalRoundResult(BaseModel):
    round_number: int
    focus: str = ""
    queries: list[RetrievalQuery] = Field(default_factory=list)
    sources_found: list[Source] = Field(default_factory=list)
    findings_summary: str = ""
    new_entities: list[Entity] = Field(default_factory=list)
    new_relationships: list[Relationship] = Field(default_factory=list)
    next_round_triggers: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Event Framing
# ---------------------------------------------------------------------------

class EventFraming(BaseModel):
    core_event: str = ""
    variants: list[str] = Field(default_factory=list)
    who: list[str] = Field(default_factory=list)
    what: str = ""
    when: str = ""
    where: list[str] = Field(default_factory=list)
    why: str = ""
    how: str = ""
    so_what: str = ""
    investigation_questions: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Analysis Outputs
# ---------------------------------------------------------------------------

class ActorProfile(BaseModel):
    name: str
    role: str = ""
    motivations: list[str] = Field(default_factory=list)
    historical_patterns: list[str] = Field(default_factory=list)
    relationships: list[str] = Field(default_factory=list)
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM


class CausalLink(BaseModel):
    cause: str
    effect: str
    confidence: ConfidenceLevel = ConfidenceLevel.MEDIUM
    sources: list[Source] = Field(default_factory=list)


class Scenario(BaseModel):
    title: str
    description: str
    probability: str = ""  # e.g. "Medium-High"
    key_indicators: list[str] = Field(default_factory=list)
    stakeholder_impacts: dict[str, str] = Field(default_factory=dict)


class AnalysisResult(BaseModel):
    actor_profiles: list[ActorProfile] = Field(default_factory=list)
    causal_chains: list[CausalLink] = Field(default_factory=list)
    hidden_connections: list[str] = Field(default_factory=list)
    contradictions: list[str] = Field(default_factory=list)
    scenarios: list[Scenario] = Field(default_factory=list)
    key_questions_remaining: list[str] = Field(default_factory=list)
    confidence_assessment: str = ""


# ---------------------------------------------------------------------------
# Intelligence Report
# ---------------------------------------------------------------------------

class IntelligenceReport(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    title: str = ""
    executive_summary: str = ""
    event_overview: str = ""
    key_actors_analysis: str = ""
    deep_background: str = ""
    hidden_connections: str = ""
    analytical_assessment: str = ""
    scenarios_and_implications: str = ""
    confidence_assessment: str = ""
    key_questions_remaining: str = ""
    sources_and_citations: str = ""
    generated_at: datetime = Field(default_factory=datetime.utcnow)


# ---------------------------------------------------------------------------
# Analysis Session (top-level container)
# ---------------------------------------------------------------------------

class AnalysisSession(BaseModel):
    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:16])
    user_input: str = ""
    status: AnalysisStatus = AnalysisStatus.PENDING
    framing: EventFraming | None = None
    retrieval_rounds: list[RetrievalRoundResult] = Field(default_factory=list)
    entities: list[Entity] = Field(default_factory=list)
    relationships: list[Relationship] = Field(default_factory=list)
    analysis: AnalysisResult | None = None
    report: IntelligenceReport | None = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    progress_messages: list[str] = Field(default_factory=list)
    error: str | None = None
