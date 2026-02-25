"""Application configuration using pydantic-settings."""

import platform
from pathlib import Path

from pydantic_settings import BaseSettings

# Resolve the project root (three levels up from core/config.py) so that
# relative paths like "reports_output" resolve correctly regardless of the
# working directory or platform (Windows / macOS / Linux).
_PROJECT_ROOT = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """Global application settings loaded from environment variables."""

    app_name: str = "Deep Intelligence Analysis Platform"
    app_version: str = "1.0.0"
    debug: bool = False

    # LLM Configuration
    llm_provider: str = "anthropic"  # "anthropic" or "openai"
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    openai_api_key: str = ""
    openai_model: str = "gpt-4o"
    llm_max_tokens: int = 4096
    llm_temperature: float = 0.3

    # Retrieval Configuration
    search_provider: str = "tavily"  # "tavily" or "bing"
    tavily_api_key: str = ""
    bing_api_key: str = ""
    max_search_results_per_query: int = 10
    max_retrieval_rounds: int = 5

    # Neo4j Knowledge Graph
    neo4j_uri: str = "bolt://localhost:7687"
    neo4j_user: str = "neo4j"
    neo4j_password: str = ""

    # Report output — resolved to an absolute, platform-correct path via
    # the reports_output_path property below.
    reports_output_dir: str = "reports_output"

    # Server — on Windows default to 127.0.0.1 (localhost-only); on
    # Linux/macOS default to 0.0.0.0 (all interfaces, needed for Docker).
    host: str = "127.0.0.1" if platform.system() == "Windows" else "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {
        "env_file": str(_PROJECT_ROOT / "backend" / ".env"),
        "env_file_encoding": "utf-8",
    }

    @property
    def reports_output_path(self) -> Path:
        """Return an absolute Path for the reports output directory.

        Works correctly on both Windows (backslash paths) and Unix.
        """
        p = Path(self.reports_output_dir)
        if p.is_absolute():
            return p
        return _PROJECT_ROOT / p


settings = Settings()
