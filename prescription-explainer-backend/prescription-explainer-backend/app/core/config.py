import os
from functools import lru_cache

from dotenv import load_dotenv

load_dotenv()


class Settings:
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/prescription_db"
    )

    # Gemma
    GEMMA_API_URL: str = os.getenv("GEMMA_API_URL", "http://localhost:11434/api/generate")
    GEMMA_MODEL_NAME: str = os.getenv("GEMMA_MODEL_NAME", "gemma-4")

    # OCR
    OCR_ENGINE: str = os.getenv("OCR_ENGINE", "tesseract")  # or "gemma_vision"

    # Uploads
    UPLOAD_DIR: str = os.getenv("UPLOAD_DIR", "uploads")
    MAX_UPLOAD_SIZE_MB: int = int(os.getenv("MAX_UPLOAD_SIZE_MB", "10"))


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()