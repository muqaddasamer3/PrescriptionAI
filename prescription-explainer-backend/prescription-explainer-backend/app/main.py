from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

from app.core.config import settings
from app.core.database import Base, engine
from app.routers import prescription
from app.utils.logger import logger
from app.utils.response import error_response


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.PROJECT_VERSION,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(prescription.router, prefix="/api/v1/prescriptions", tags=["Prescriptions"])
    return app


@app.get("/")
def health_check():
    return {"status": "ok", "service": "prescription-explainer-backend"}