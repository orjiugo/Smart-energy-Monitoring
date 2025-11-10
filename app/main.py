# app/main.py
"""FastAPI application factory and configuration"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.utils.logger import get_logger
from app.api.routes.energy import router as energy_router

logger = get_logger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Starting Smart Energy Monitoring API v{settings.api_version}")
    yield
    logger.info("Shutting down Smart Energy Monitoring API")

def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.api_title,
        version=settings.api_version,
        description="Real-time IoT smart energy monitoring with AI-powered forecasting",
        lifespan=lifespan,
    )

    # ✅ Register API routers here
    app.include_router(energy_router)

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "message": "Smart Energy Monitoring API",
            "version": settings.api_version,
            "docs": "/docs",
        }

    return app

# ASGI app instance for Uvicorn
app = create_app()

if __name__ == "__main__":
    import uvicorn
    # Note: in Docker we usually start Uvicorn via the command, but this keeps local runs working too.
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=False)
