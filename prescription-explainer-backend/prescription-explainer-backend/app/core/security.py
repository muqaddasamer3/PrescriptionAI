from fastapi import Header, HTTPException
from starlette.status import HTTP_401_UNAUTHORIZED

from app.core.config import settings


def validate_api_key(x_api_key: str | None = Header(None)) -> str | None:
    if settings.API_KEY and x_api_key != settings.API_KEY:
        raise HTTPException(
            status_code=HTTP_401_UNAUTHORIZED,
            detail="Invalid API key.",
        )
    return x_api_key
