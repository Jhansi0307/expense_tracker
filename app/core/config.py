import os
from functools import lru_cache
from dotenv import load_dotenv
from pydantic import BaseSettings

# Load .env if present
load_dotenv()

class Settings(BaseSettings):
    PROJECT_NAME: str = "Expense Tracker API"
    ENVIRONMENT: str = "local"

    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "expense_user")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "expense_password")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "expense_db")
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")

    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "change-me")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return (
            f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}"
            f"@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        )

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings()
