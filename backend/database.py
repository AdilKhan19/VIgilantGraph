"""
VigilantGraph database configuration.

Uses SQLite for local development.
The SQLAlchemy architecture can later support PostgreSQL.
"""

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

# Store the database inside the project, not in a temporary directory.
PROJECT_ROOT = Path(__file__).resolve().parent.parent
DATA_DIRECTORY = PROJECT_ROOT / "data"
DATA_DIRECTORY.mkdir(parents=True, exist_ok=True)

DATABASE_FILE = DATA_DIRECTORY / "vigilantgraph.db"
DATABASE_URL = f"sqlite:///{DATABASE_FILE.as_posix()}"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
)


class Base(DeclarativeBase):
    """Base class for all database models."""


def get_db():
    """Provide a database session to an API request."""

    database = SessionLocal()

    try:
        yield database
    finally:
        database.close()


def init_db():
    """Create database tables that do not already exist."""

    # Import models so SQLAlchemy registers their table definitions.
    import backend.models  # noqa: F401

    Base.metadata.create_all(bind=engine)