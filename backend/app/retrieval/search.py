"""Web search abstraction layer.

Supports Tavily and Bing as search providers.  Returns normalised Source
objects.
"""

from __future__ import annotations

import logging
from urllib.parse import urlparse

import httpx

from ..core.config import settings
from ..core.models import Source, SourceTier

logger = logging.getLogger(__name__)

# Simple heuristic for source tier assignment
_TIER1_DOMAINS = {
    "reuters.com", "apnews.com", "gov", "sec.gov", "un.org",
    "who.int", "worldbank.org",
}
_TIER2_DOMAINS = {
    "nytimes.com", "washingtonpost.com", "bbc.com", "bbc.co.uk",
    "economist.com", "ft.com", "theguardian.com", "wsj.com",
    "bloomberg.com", "aljazeera.com",
}


def _classify_source(domain: str) -> SourceTier:
    domain_lower = domain.lower()
    for d in _TIER1_DOMAINS:
        if domain_lower.endswith(d):
            return SourceTier.OFFICIAL
    for d in _TIER2_DOMAINS:
        if domain_lower.endswith(d):
            return SourceTier.ESTABLISHED
    if domain_lower.endswith(".edu") or domain_lower.endswith(".org"):
        return SourceTier.SECONDARY
    return SourceTier.UNVERIFIED


async def web_search(query: str, max_results: int | None = None) -> list[Source]:
    """Execute a web search and return normalised Source objects."""

    n = max_results or settings.max_search_results_per_query
    provider = settings.search_provider

    if provider == "tavily":
        return await _tavily_search(query, n)
    elif provider == "bing":
        return await _bing_search(query, n)
    else:
        raise ValueError(f"Unsupported search provider: {provider}")


async def _tavily_search(query: str, max_results: int) -> list[Source]:
    """Search using the Tavily API."""

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.post(
            "https://api.tavily.com/search",
            json={
                "api_key": settings.tavily_api_key,
                "query": query,
                "max_results": max_results,
                "include_raw_content": False,
                "search_depth": "advanced",
            },
        )
        resp.raise_for_status()
        data = resp.json()

    sources: list[Source] = []
    for r in data.get("results", []):
        domain = urlparse(r.get("url", "")).netloc
        sources.append(
            Source(
                url=r.get("url", ""),
                title=r.get("title", ""),
                domain=domain,
                tier=_classify_source(domain),
                snippet=r.get("content", "")[:500],
            )
        )
    return sources


async def _bing_search(query: str, max_results: int) -> list[Source]:
    """Search using the Bing Web Search API."""

    headers = {"Ocp-Apim-Subscription-Key": settings.bing_api_key}
    params = {"q": query, "count": max_results, "textDecorations": False}

    async with httpx.AsyncClient(timeout=30) as client:
        resp = await client.get(
            "https://api.bing.microsoft.com/v7.0/search",
            headers=headers,
            params=params,
        )
        resp.raise_for_status()
        data = resp.json()

    sources: list[Source] = []
    for r in data.get("webPages", {}).get("value", []):
        domain = urlparse(r.get("url", "")).netloc
        sources.append(
            Source(
                url=r.get("url", ""),
                title=r.get("name", ""),
                domain=domain,
                tier=_classify_source(domain),
                snippet=r.get("snippet", "")[:500],
            )
        )
    return sources
