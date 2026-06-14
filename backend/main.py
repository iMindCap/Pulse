"""
Pulse - Main Application

Entry point for the Pulse backend server.
"""

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from config import settings
from db import init_db
from api import router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Runs on startup and shutdown of the application."""
    # Startup: create data directory for the database
    data_dir = Path(settings.DATABASE_PATH).parent
    data_dir.mkdir(parents=True, exist_ok=True)
    await init_db()
    print(f"⚡ Pulse v{settings.APP_VERSION} is running")
    print(f"📁 Data directory: {data_dir}")
    yield
    # Shutdown
    print("👋 Pulse is shutting down")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="One dashboard. Full visibility. Zero config.",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Allow frontend to communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register API routes
app.include_router(router)

# Serve frontend static files in production
STATIC_DIR = Path(__file__).parent / "static"

if STATIC_DIR.exists():
    app.mount("/assets", StaticFiles(directory=STATIC_DIR / "assets"), name="assets")

    @app.get("/{path:path}")
    async def serve_frontend(path: str):
        """Serve Vue frontend for all non-API routes."""
        file_path = STATIC_DIR / path
        if file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(STATIC_DIR / "index.html")
else:
    @app.get("/")
    async def root():
        """Root endpoint when running backend only (development)."""
        return {
            "name": settings.APP_NAME,
            "version": settings.APP_VERSION,
            "status": "running",
            "docs": "/docs",
        }


@app.get("/health")
async def health_check():
    """Health check endpoint to verify the server is alive."""
    return {"status": "healthy"}