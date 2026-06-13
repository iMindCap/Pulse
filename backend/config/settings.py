"""
Pulse - Application Settings

Centralized configuration for the Pulse application.
All settings can be overridden via environment variables.
"""

import os
from pathlib import Path


# Base directory
BASE_DIR = Path(__file__).resolve().parent.parent

# App info
APP_NAME = "Pulse"
APP_VERSION = "0.1.0"

# Server
HOST = os.getenv("PULSE_HOST", "0.0.0.0")
PORT = int(os.getenv("PULSE_PORT", "8000"))

# Database
DATABASE_PATH = os.getenv(
    "PULSE_DB_PATH",
    str(BASE_DIR / "data" / "pulse.db")
)

# Collection intervals (in seconds)
SYSTEM_COLLECT_INTERVAL = int(os.getenv("PULSE_SYSTEM_INTERVAL", "5"))
DOCKER_COLLECT_INTERVAL = int(os.getenv("PULSE_DOCKER_INTERVAL", "10"))
PING_COLLECT_INTERVAL = int(os.getenv("PULSE_PING_INTERVAL", "30"))

# Docker
DOCKER_SOCKET = os.getenv("PULSE_DOCKER_SOCKET", "unix:///var/run/docker.sock")

# CORS (allowed origins for frontend)
CORS_ORIGINS = os.getenv("PULSE_CORS_ORIGINS", "http://localhost:5173").split(",")