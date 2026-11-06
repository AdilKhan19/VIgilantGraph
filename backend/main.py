
"""
VigilantGraph
Enterprise Network Attack Graph & Predictive Risk Intelligence

Main application entry point.
"""

from datetime import UTC, datetime

from fastapi import FastAPI

# Initialize the application
app = FastAPI(
    title="VigilantGraph",
    description=(
        "An algorithmic network attack graph, "
        "risk propagation and predictive analytics platform."
    ),
    version="0.1.0",
)


@app.get("/")
def root():
    """Return basic application information."""

    return {
        "application": "VigilantGraph",
        "version": "0.1.0",
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
    """Return current system information."""

    return {
        "project": "VigilantGraph",
        "architecture": "Modular Analytics Engine",
        "modules": [
            "Network Discovery",
            "Asset Intelligence",
            "Vulnerability Intelligence",
            "Attack Graph Engine",
            "Bayesian Risk Engine",
            "HMM Prediction Engine",
            "Pathfinding Engine",
            "Centrality Analysis",
            "Patch Optimization",
            "Anomaly Detection",
            "Game Theory Simulation",
            "Analytics Dashboard",
        ],
        "environment": "Development",
    }