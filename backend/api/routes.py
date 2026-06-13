"""
Pulse - API Routes

Defines all REST API endpoints for the Pulse dashboard.
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from collectors import get_system_metrics, get_docker_info, get_containers, check_services
from db import fetch_all, fetch_one, execute_query


router = APIRouter(prefix="/api")


# ──────────────────────────────────────────
# Schemas
# ──────────────────────────────────────────

class ServiceCreate(BaseModel):
    """Schema for creating a new service to monitor."""
    name: str
    url: str
    check_type: str = "http"


# ──────────────────────────────────────────
# System Metrics
# ──────────────────────────────────────────

@router.get("/system")
async def system_metrics():
    """Get current system metrics (CPU, memory, disk, temperature)."""
    metrics = await get_system_metrics()
    return metrics


# ──────────────────────────────────────────
# Docker
# ──────────────────────────────────────────

@router.get("/docker")
async def docker_info():
    """Get general Docker engine information."""
    info = await get_docker_info()
    return info


@router.get("/containers")
async def containers_list():
    """Get status and stats for all Docker containers."""
    containers = await get_containers()
    return {"containers": containers, "count": len(containers)}


# ──────────────────────────────────────────
# Services
# ──────────────────────────────────────────

@router.get("/services")
async def services_list():
    """Get all monitored services with their current status."""
    services = await fetch_all(
        "SELECT * FROM services WHERE is_active = 1"
    )

    if not services:
        return {"services": [], "count": 0}

    # Check current status of each service
    results = await check_services(services)
    return {"services": results, "count": len(results)}


@router.post("/services")
async def service_create(service: ServiceCreate):
    """Add a new service to monitor."""
    # Check if service name already exists
    existing = await fetch_one(
        "SELECT * FROM services WHERE name = ?",
        (service.name,)
    )
    if existing:
        raise HTTPException(status_code=400, detail="Service name already exists")

    await execute_query(
        "INSERT INTO services (name, url, check_type) VALUES (?, ?, ?)",
        (service.name, service.url, service.check_type)
    )

    return {"message": f"Service '{service.name}' added successfully"}


@router.delete("/services/{service_id}")
async def service_delete(service_id: int):
    """Remove a service from monitoring."""
    existing = await fetch_one(
        "SELECT * FROM services WHERE id = ?",
        (service_id,)
    )
    if not existing:
        raise HTTPException(status_code=404, detail="Service not found")

    await execute_query(
        "UPDATE services SET is_active = 0 WHERE id = ?",
        (service_id,)
    )

    return {"message": f"Service removed successfully"}