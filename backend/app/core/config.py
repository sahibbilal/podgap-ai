from pydantic_settings import BaseSettings
from pydantic import Field
from functools import lru_cache


class Settings(BaseSettings):
    # App
    api_v1_prefix: str = "/api/v1"
    project_name: str = "PodGap AI"
    # Store as string so .env comma-separated value is not parsed as JSON; use backend_cors_origins property for list
    backend_cors_origins_str: str = Field(
        default="http://localhost:3000,http://127.0.0.1:3000,http://localhost:3001,http://127.0.0.1:3001,http://localhost:3002,http://127.0.0.1:3002",
        validation_alias="BACKEND_CORS_ORIGINS",
    )

    @property
    def backend_cors_origins(self) -> list[str]:
        return [x.strip() for x in self.backend_cors_origins_str.split(",") if x.strip()]

    # Database: default SQLite (no build tools needed). For PostgreSQL set DATABASE_URL and install asyncpg.
    database_url: str = Field(default="sqlite+aiosqlite:///./podgap.db", validation_alias="DATABASE_URL")

    def get_database_url_async(self) -> str:
        u = self.database_url
        if u.startswith("postgresql://"):
            return u.replace("postgresql://", "postgresql+asyncpg://", 1)
        return u

    # Redis
    redis_url: str = Field(default="redis://localhost:6379/0", validation_alias="REDIS_URL")

    # Celery
    celery_broker_url: str = Field(default="amqp://guest:guest@localhost:5672//", validation_alias="CELERY_BROKER_URL")

    # Ollama
    ollama_host: str = "http://localhost:11434"
    ollama_embed_model: str = "nomic-embed-text"
    ollama_llm_model: str = "llama3.2"

    # Listen Notes
    listen_notes_api_key: str = ""

    # YouTube Data API
    youtube_data_api_key: str = ""

    # Reddit (optional)
    reddit_client_id: str = ""
    reddit_client_secret: str = ""
    reddit_user_agent: str = "PodGapAI/1.0"

    # JWT
    jwt_secret: str = Field(default="change-me-in-production-min-32-chars", validation_alias="JWT_SECRET")
    jwt_algorithm: str = Field(default="HS256", validation_alias="JWT_ALGORITHM")
    jwt_expire_minutes: int = Field(default=60, validation_alias="JWT_EXPIRE_MINUTES")

    model_config = {"env_file": ".env", "extra": "ignore"}


@lru_cache
def get_settings() -> Settings:
    return Settings()
