"""Event Framing & Scoping Agent.

Decomposes a user-provided event or topic into structured analytical
dimensions (Who/What/When/Where/Why/How/So-What) and generates an
investigation blueprint of questions to answer.
"""

from __future__ import annotations

import logging

from backend.app.core.llm import chat_completion_json
from backend.app.core.models import EventFraming

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """\
You are an expert intelligence analyst responsible for the initial scoping and
framing of an event or topic.  Your job is to decompose the input into
structured analytical dimensions and produce a rigorous investigation
blueprint.

Return your answer as a JSON object with exactly these keys:
{
  "core_event": "<one-sentence description of the core event>",
  "variants": ["<alternate names, hashtags, regional angles>"],
  "who": ["<key actors / organisations involved>"],
  "what": "<what happened or is happening>",
  "when": "<timeline / date range>",
  "where": ["<relevant geographies>"],
  "why": "<initial hypotheses on motivations>",
  "how": "<mechanisms / methods involved>",
  "so_what": "<why this matters — stakes and significance>",
  "investigation_questions": [
    "<targeted analytical question 1>",
    "<targeted analytical question 2>",
    "..."
  ]
}

Rules:
- investigation_questions should contain 8-15 questions that drive deeper
  retrieval — not surface-level.  Think like an intelligence analyst.
- All fields must be populated; use "Unknown — requires investigation" if
  genuinely unknown.
- Be precise and specific rather than generic.
"""


async def frame_event(user_input: str) -> EventFraming:
    """Decompose user input into an EventFraming structure."""

    logger.info("Framing event: %s", user_input[:120])

    data = await chat_completion_json(
        system_prompt=SYSTEM_PROMPT,
        user_prompt=f"Analyze and frame the following event or topic:\n\n{user_input}",
        temperature=0.2,
    )

    return EventFraming(**data)
