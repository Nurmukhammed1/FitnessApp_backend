from pydantic import Field, model_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FitnessApp"
    DATABASE_URL: str = Field(
        default="sqlite+aiosqlite:///./fitness.db",
        description="Async database connection string (use postgresql+asyncpg://... for production)",
    )
    SECRET_KEY: str = "change-me-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    @model_validator(mode="after")
    def fix_database_url(self):
        """Convert Render's postgres:// to postgresql+asyncpg:// automatically."""
        url = self.DATABASE_URL
        if url.startswith("postgres://"):
            self.DATABASE_URL = url.replace("postgres://", "postgresql+asyncpg://", 1)
        elif url.startswith("postgresql://"):
            self.DATABASE_URL = url.replace("postgresql://", "postgresql+asyncpg://", 1)
        return self

    class Config:
        env_file = ".env"


settings = Settings()
