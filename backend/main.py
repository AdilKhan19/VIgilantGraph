"""
VigilantGraph
Enterprise Network Attack Graph & Predictive Risk Intelligence

Main application entry point.
"""

from contextlib import asynccontextmanager
from datetime import UTC, datetime
from typing import Annotated

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from backend.asset_inventory import collect_local_asset
from backend.asset_repository import list_assets, save_asset
from backend.database import get_db, init_db


@asynccontextmanager
async def lifespan(application: FastAPI):
    """Initialize persistent storage when the API starts."""

    init_db()
    yield


app = FastAPI(
    title="VigilantGraph",
    description=(
        "An algorithmic network attack graph, "
        "risk propagation and predictive analytics platform."
    ),
    version="0.2.0",
    lifespan=lifespan,
)


def serialize_asset(asset):
    """Convert a database asset record into JSON-compatible data."""

    return {
        "id": asset.id,
        "asset_key": asset.asset_key,
        "hostname": asset.hostname,
        "operating_system": asset.operating_system,
        "os_release": asset.os_release,
        "os_version": asset.os_version,
        "architecture": asset.architecture,
        "processor": asset.processor,
        "cpu_logical_cores": asset.cpu_logical_cores,
        "memory_total_bytes": asset.memory_total_bytes,
        "memory_available_bytes": asset.memory_available_bytes,
        "network_interfaces": asset.network_interfaces,
        "disks": asset.disks,
        "source": asset.source,
        "verification_status": asset.verification_status,
        "collection_timestamp": asset.collection_timestamp.isoformat(),
        "first_seen": asset.first_seen.isoformat(),
        "last_seen": asset.last_seen.isoformat(),
    }


@app.get("/")
def root():
    """Return basic application information."""

    return {
        "application": "VigilantGraph",
        "version": "0.2.0",
        "status": "operational",
        "description": (
            "Enterprise Network Attack Graph "
            "& Predictive Risk Intelligence Engine"
        ),
    }


@app.get("/health")
def health_check():
    """Check whether the backend is operational."""

    return {
        "status": "healthy",
        "timestamp": datetime.now(UTC).isoformat(),
        "service": "VigilantGraph Backend",
    }


@app.get("/api/v1/system/info")
def system_info():
    """Return implemented and planned system modules."""

    return {
        "project": "VigilantGraph",
        "architecture": "Modular Analytics Engine",
        "implemented_modules": [
            "Local Asset Inventory",
            "Persistent Asset Registry",
            "Graph Engine",
            "Pathfinding Engine",
            "Bayesian Risk Propagation",
            "Risk Scoring",
        ],
        "planned_modules": [
            "Authorized Network Discovery",
            "Vulnerability Intelligence",
            "HMM Prediction Engine",
            "Centrality Analysis",
            "Patch Optimization",
            "Anomaly Detection",
            "Controlled Remediation",
            "Analytics Dashboard",
        ],
        "environment": "Development",
    }


@app.get("/api/v1/assets/local")
def get_local_asset():
    """Return current inventory of the machine running VigilantGraph."""

    return {
        "status": "success",
        "asset": collect_local_asset(),
    }


@app.post("/api/v1/assets/local/collect")
def collect_and_save_local_asset(
    database: Annotated[Session, Depends(get_db)],
):
    """Collect local machine inventory and save it to the database."""

    asset_data = collect_local_asset()
    saved_asset = save_asset(database, asset_data)

    return {
        "status": "success",
        "message": "Local asset inventory saved successfully.",
        "asset": serialize_asset(saved_asset),
    }


@app.get("/api/v1/assets")
def get_saved_assets(
    database: Annotated[Session, Depends(get_db)],
):
    """Return all assets saved in the registry."""

    assets = list_assets(database)

    return {
        "status": "success",
        "count": len(assets),
        "assets": [
            serialize_asset(asset)
            for asset in assets
        ],
    }