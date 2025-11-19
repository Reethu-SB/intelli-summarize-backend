"""Database configuration for Intelli Summarize.

Loads DB settings from a `.env` file (via python-dotenv) and exposes the
SQLAlchemy `engine`, `SessionLocal`, `Base`, and a `get_db()` dependency
for use in routers.

Supports an explicit `DATABASE_URL` env var, otherwise will build a MySQL
URL from `DB_USER`, `DB_PASSWORD`, `DB_HOST`, `DB_PORT`, `DB_NAME`.
If `DB_ENGINE` is set to `sqlite` or `TESTING` is `1`, a local SQLite DB
is used (useful for tests).
"""

import os
from typing import Generator

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


# Load environment variables from .env (if present)
load_dotenv()

# Allow full DATABASE_URL override (e.g. for production/staging)
DATABASE_URL = os.getenv("DATABASE_URL")

# If DATABASE_URL not provided, decide between MySQL and SQLite
if not DATABASE_URL:
    use_sqlite = os.getenv("DB_ENGINE", "").lower() == "sqlite" or os.getenv("TESTING") == "1"
    if use_sqlite:
        # SQLite - suitable for local development / tests
        DATABASE_URL = "sqlite:///./test.db"
        connect_args = {"check_same_thread": False}
    else:
        # Build a MySQL URL from individual env vars
        user = os.getenv("DB_USER", "root")
        password = os.getenv("DB_PASSWORD", "")
        host = os.getenv("DB_HOST", "localhost")
        port = os.getenv("DB_PORT", "3306")
        name = os.getenv("DB_NAME", "intelli_summarize")
        # using PyMySQL driver; adjust if you use a different MySQL driver
        DATABASE_URL = f"mysql+pymysql://{user}:{password}@{host}:{port}/{name}?charset=utf8mb4"
        connect_args = {}
else:
    # If a full URL is provided, don't pass special connect_args by default
    connect_args = {}


# Create SQLAlchemy engine
engine = create_engine(DATABASE_URL, pool_pre_ping=True, connect_args=connect_args)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for declarative models
Base = declarative_base()


def get_db() -> Generator:
    """FastAPI dependency that yields a SQLAlchemy session and ensures it's closed.

    Usage in routers:
        from fastapi import Depends
        from database import get_db

        def endpoint(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
