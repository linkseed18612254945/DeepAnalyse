"""LLM client abstraction — supports Anthropic and OpenAI backends."""

from __future__ import annotations

import json
import logging
from typing import Any

import anthropic
import openai

from .config import settings

logger = logging.getLogger(__name__)


async def chat_completion(
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float | None = None,
    max_tokens: int | None = None,
    response_json: bool = False,
) -> str:
    """Send a prompt to the configured LLM and return the text response."""

    temp = temperature if temperature is not None else settings.llm_temperature
    tokens = max_tokens if max_tokens is not None else settings.llm_max_tokens
    provider = settings.llm_provider

    if provider == "anthropic":
        return await _anthropic_chat(system_prompt, user_prompt, temp, tokens)
    elif provider == "openai":
        return await _openai_chat(
            system_prompt, user_prompt, temp, tokens, response_json
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {provider}")


async def chat_completion_json(
    system_prompt: str,
    user_prompt: str,
    *,
    temperature: float | None = None,
    max_tokens: int | None = None,
) -> dict[str, Any]:
    """Request a JSON response from the LLM and parse it."""

    raw = await chat_completion(
        system_prompt,
        user_prompt,
        temperature=temperature,
        max_tokens=max_tokens,
        response_json=True,
    )

    # Strip markdown code fences if present
    text = raw.strip()
    if text.startswith("```"):
        lines = text.split("\n")
        lines = [l for l in lines if not l.strip().startswith("```")]
        text = "\n".join(lines)

    return json.loads(text)


# ---------------------------------------------------------------------------
# Provider implementations
# ---------------------------------------------------------------------------

async def _anthropic_chat(
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
) -> str:
    client = anthropic.AsyncAnthropic(api_key=settings.anthropic_api_key)
    message = await client.messages.create(
        model=settings.anthropic_model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text


async def _openai_chat(
    system_prompt: str,
    user_prompt: str,
    temperature: float,
    max_tokens: int,
    response_json: bool,
) -> str:
    client = openai.AsyncOpenAI(api_key=settings.openai_api_key)
    kwargs: dict[str, Any] = {}
    if response_json:
        kwargs["response_format"] = {"type": "json_object"}

    response = await client.chat.completions.create(
        model=settings.openai_model,
        temperature=temperature,
        max_tokens=max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        **kwargs,
    )
    return response.choices[0].message.content or ""
