"""Analysis & Synthesis Agent.

Transforms retrieved facts and entities into deep intelligence insights:
actor profiles, causal chains, hidden connections, contradictions, and
forward-looking scenarios.
"""

from __future__ import annotations

import logging

from backend.app.core.llm import chat_completion_json
from backend.app.core.models import (
    AnalysisResult,
    ActorProfile,
    CausalLink,
    Entity,
    EventFraming,
    Relationship,
    RetrievalRoundResult,
    Scenario,
)

logger = logging.getLogger(__name__)

ANALYSIS_SYSTEM_PROMPT = """\
You are a senior intelligence analyst producing a deep analytical assessment.
You will receive structured findings from multiple retrieval rounds, extracted
entities, and relationships.

Produce a JSON object with these keys:

{{
  "actor_profiles": [
    {{
      "name": "<actor name>",
      "role": "<role in this event>",
      "motivations": ["<inferred motivation>", ...],
      "historical_patterns": ["<past behaviour pattern>", ...],
      "relationships": ["<key relationship descriptions>", ...],
      "confidence": "high|medium|low|speculative"
    }}
  ],
  "causal_chains": [
    {{
      "cause": "<cause>",
      "effect": "<effect>",
      "confidence": "high|medium|low|speculative"
    }}
  ],
  "hidden_connections": [
    "<description of a non-obvious connection>",
    ...
  ],
  "contradictions": [
    "<description of a contradiction between sources or stated vs actual positions>",
    ...
  ],
  "scenarios": [
    {{
      "title": "<scenario name>",
      "description": "<2-3 sentence description>",
      "probability": "<Low|Medium-Low|Medium|Medium-High|High>",
      "key_indicators": ["<signal that this scenario is unfolding>", ...],
      "stakeholder_impacts": {{"<stakeholder>": "<impact>", ...}}
    }}
  ],
  "key_questions_remaining": [
    "<unresolved question>",
    ...
  ],
  "confidence_assessment": "<overall confidence paragraph>"
}}

Guidelines:
- Produce 3-5 forward-looking scenarios grounded in evidence.
- Go at least 3 levels deep in causal chains.
- Identify what is *not* being said (silence analysis).
- Cross-reference actor statements against their actions.
- Generate 3-8 actor profiles for the most important actors.
- Be analytical, not merely descriptive.
"""


async def run_analysis(
    framing: EventFraming,
    retrieval_rounds: list[RetrievalRoundResult],
    entities: list[Entity],
    relationships: list[Relationship],
) -> AnalysisResult:
    """Run deep analysis on all gathered intelligence."""

    logger.info("Running deep analysis synthesis")

    # Build context from all retrieval rounds
    context_parts = [
        f"# Event: {framing.core_event}\n",
        f"**What:** {framing.what}",
        f"**Who:** {', '.join(framing.who)}",
        f"**Where:** {', '.join(framing.where)}",
        f"**When:** {framing.when}",
        f"**Why:** {framing.why}",
        f"**How:** {framing.how}",
        f"**Significance:** {framing.so_what}\n",
    ]

    for rr in retrieval_rounds:
        context_parts.append(f"## Retrieval Round {rr.round_number}: {rr.focus}")
        context_parts.append(rr.findings_summary)
        if rr.next_round_triggers:
            context_parts.append(f"Triggers: {'; '.join(rr.next_round_triggers)}")
        context_parts.append("")

    if entities:
        context_parts.append("## Extracted Entities")
        for e in entities[:50]:
            context_parts.append(f"- **{e.name}** ({e.entity_type}): {e.description}")
        context_parts.append("")

    if relationships:
        context_parts.append("## Extracted Relationships")
        for r in relationships[:50]:
            src = next((e.name for e in entities if e.id == r.source_entity_id), r.source_entity_id)
            tgt = next((e.name for e in entities if e.id == r.target_entity_id), r.target_entity_id)
            context_parts.append(f"- {src} —[{r.relationship_type}]→ {tgt}: {r.description}")

    context = "\n".join(context_parts)

    data = await chat_completion_json(
        system_prompt=ANALYSIS_SYSTEM_PROMPT,
        user_prompt=context,
        max_tokens=4096,
        temperature=0.3,
    )

    # Parse into structured models
    actor_profiles = [ActorProfile(**a) for a in data.get("actor_profiles", [])]
    causal_chains = [CausalLink(**c) for c in data.get("causal_chains", [])]
    scenarios = [Scenario(**s) for s in data.get("scenarios", [])]

    return AnalysisResult(
        actor_profiles=actor_profiles,
        causal_chains=causal_chains,
        hidden_connections=data.get("hidden_connections", []),
        contradictions=data.get("contradictions", []),
        scenarios=scenarios,
        key_questions_remaining=data.get("key_questions_remaining", []),
        confidence_assessment=data.get("confidence_assessment", ""),
    )
