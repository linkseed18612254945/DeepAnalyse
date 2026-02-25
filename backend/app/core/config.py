"""Application configuration using pydantic-settings."""

from pydantic_settings import BaseSettings


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

    # Report output
    reports_output_dir: str = "reports_output"

    # Server
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: list[str] = ["http://localhost:5173", "http://localhost:3000"]

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
