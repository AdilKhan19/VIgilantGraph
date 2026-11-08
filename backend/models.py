"""
VigilantGraph database models.
"""

from datetime import UTC, datetime

from sqlalchemy import JSON, DateTime, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from backend.database import Base


class Asset(Base):
    """A computer or server recorded in the asset inventory."""

    __tablename__ = "assets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True,
    )

    asset_key: Mapped[str] = mapped_column(
        String(64),
        unique=True,
        index=True,
        nullable=False,
    )

    hostname: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    operating_system: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    os_release: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    os_version: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    architecture: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    processor: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    cpu_logical_cores: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True,
    )

    memory_total_bytes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    memory_available_bytes: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    network_interfaces: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    disks: Mapped[list] = mapped_column(
        JSON,
        nullable=False,
    )

    source: Mapped[str] = mapped_column(
        String(100),
        default="local_collector",
        nullable=False,
    )

    verification_status: Mapped[str] = mapped_column(
        String(50),
        default="collected",
        nullable=False,
    )

    collection_timestamp: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    first_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        nullable=False,
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(UTC),
        onupdate=lambda: datetime.now(UTC),
        nullable=False,
    )