from pydantic import Field
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

    class Config:
        env_file = ".env"


settings = Settings()
