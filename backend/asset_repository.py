"""
Database operations for asset inventory.
"""

import hashlib
from datetime import UTC, datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from backend.models import Asset


def create_asset_key(asset_data: dict) -> str:
    """Generate a deterministic initial identity for an asset."""

    identity = "|".join(
        [
            asset_data["hostname"].strip().lower(),
            asset_data["operating_system"].strip().lower(),
            asset_data["architecture"].strip().lower(),
        ]
    )

    return hashlib.sha256(identity.encode("utf-8")).hexdigest()


def save_asset(database: Session, asset_data: dict) -> Asset:
    """Insert a new asset or update its existing inventory record."""

    asset_key = create_asset_key(asset_data)

    asset = database.scalar(
        select(Asset).where(Asset.asset_key == asset_key)
    )

    collection_timestamp = datetime.fromisoformat(
        asset_data["collection_timestamp"]
    )

    if collection_timestamp.tzinfo is None:
        collection_timestamp = collection_timestamp.replace(tzinfo=UTC)

    fields_to_update = [
        "hostname",
        "operating_system",
        "os_release",
        "os_version",
        "architecture",
        "processor",
        "cpu_logical_cores",
        "memory_total_bytes",
        "memory_available_bytes",
        "network_interfaces",
        "disks",
    ]

    if asset is None:
        asset = Asset(
            asset_key=asset_key,
            collection_timestamp=collection_timestamp,
            source="local_collector",
            verification_status="collected",
            **{
                field: asset_data[field]
                for field in fields_to_update
            },
        )
        database.add(asset)
    else:
        for field in fields_to_update:
            setattr(asset, field, asset_data[field])

        asset.collection_timestamp = collection_timestamp
        asset.last_seen = datetime.now(UTC)

    database.commit()
    database.refresh(asset)

    return asset


def list_assets(database: Session) -> list[Asset]:
    """Return all recorded assets in stable ID order."""

    statement = select(Asset).order_by(Asset.id.asc())

    return list(database.scalars(statement).all())