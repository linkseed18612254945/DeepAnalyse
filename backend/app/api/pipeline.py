"""Orchestration pipeline — wires together all agents into a single analysis flow."""

from __future__ import annotations

import logging

from ..agents.analysis_agent import run_analysis
from ..agents.framing_agent import frame_event
from ..core.models import AnalysisSession, AnalysisStatus
from ..knowledge.graph import KnowledgeGraph
from ..report.generator import generate_report, save_report
from ..retrieval.engine import run_retrieval

logger = logging.getLogger(__name__)


async def run_full_pipeline(session: AnalysisSession, max_rounds: int = 3, output_formats: list[str] | None = None) -> AnalysisSession:
    """Execute the complete intelligence analysis pipeline.

    Stages:
    1. Event framing
    2. Multi-round retrieval
    3. Entity/relationship consolidation
    4. Deep analysis
    5. Report generation
    """

    formats = output_formats or ["markdown", "json"]
    graph = KnowledgeGraph()

    try:
        # ── Stage 1: Event Framing ───────────────────────────────────────
        session.status = AnalysisStatus.FRAMING
        session.progress_messages.append("Stage 1/5: Framing the event…")
        logger.info("[%s] Stage 1: Framing", session.id)

        session.framing = await frame_event(session.user_input)
        session.progress_messages.append(
            f"Framing complete — core event: {session.framing.core_event}"
        )

        # ── Stage 2: Multi-Round Retrieval ───────────────────────────────
        session.status = AnalysisStatus.RETRIEVING
        session.progress_messages.append("Stage 2/5: Running iterative retrieval…")
        logger.info("[%s] Stage 2: Retrieval (%d rounds)", session.id, max_rounds)

        async def _on_progress(msg: str) -> None:
            session.progress_messages.append(msg)

        async for round_result in run_retrieval(
            session.framing, max_rounds=max_rounds, on_progress=_on_progress
        ):
            session.retrieval_rounds.append(round_result)

            # Feed entities/relationships into the knowledge graph
            for entity in round_result.new_entities:
                merged = graph.add_entity(entity)
            for rel in round_result.new_relationships:
                graph.add_relationship(rel)

            session.progress_messages.append(
                f"Round {round_result.round_number} complete — "
                f"{len(round_result.sources_found)} sources, "
                f"{len(round_result.new_entities)} entities"
            )

        # ── Stage 3: Consolidate entities & relationships ────────────────
        session.status = AnalysisStatus.EXTRACTING
        session.progress_messages.append("Stage 3/5: Consolidating knowledge graph…")
        logger.info("[%s] Stage 3: Knowledge graph (%d entities, %d rels)",
                     session.id, graph.entity_count, graph.relationship_count)

        session.entities = graph.get_all_entities()
        session.relationships = graph.get_all_relationships()

        # ── Stage 4: Deep Analysis ───────────────────────────────────────
        session.status = AnalysisStatus.ANALYZING
        session.progress_messages.append("Stage 4/5: Running deep analysis…")
        logger.info("[%s] Stage 4: Analysis", session.id)

        session.analysis = await run_analysis(
            session.framing,
            session.retrieval_rounds,
            session.entities,
            session.relationships,
        )
        session.progress_messages.append("Analysis complete")

        # ── Stage 5: Report Generation ───────────────────────────────────
        session.status = AnalysisStatus.GENERATING_REPORT
        session.progress_messages.append("Stage 5/5: Generating report…")
        logger.info("[%s] Stage 5: Report", session.id)

        session.report = await generate_report(session)
        file_paths = await save_report(session.report, session.id, formats)
        session.progress_messages.append(
            f"Report saved: {', '.join(file_paths.values())}"
        )

        session.status = AnalysisStatus.COMPLETED
        session.progress_messages.append("Analysis complete ✓")
        logger.info("[%s] Pipeline complete", session.id)

    except Exception as e:
        logger.exception("[%s] Pipeline failed", session.id)
        session.status = AnalysisStatus.FAILED
        session.error = str(e)
        session.progress_messages.append(f"Error: {e}")

    return session
