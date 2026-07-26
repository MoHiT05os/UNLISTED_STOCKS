"""
Database connection and session management.
Uses SQLite for development, can be swapped to PostgreSQL later.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from contextlib import contextmanager

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from config import DATABASE_URL, DB_PATH
from db.models import Base


# ── Engine & Session Factory ──────────────────────────────
# SQLite needs check_same_thread=False for multi-threaded use
connect_args = {}
if DATABASE_URL.startswith('sqlite'):
    connect_args = {'check_same_thread': False}

engine = create_engine(
    DATABASE_URL,
    connect_args=connect_args,
    echo=False,  # Set True for SQL debug logging
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)


def init_db():
    """Create all tables if they don't exist."""
    Base.metadata.create_all(bind=engine)
    print(f'[DB] Database initialized at {DB_PATH}')


def drop_db():
    """Drop all tables (use with caution!)."""
    Base.metadata.drop_all(bind=engine)
    print('[DB] All tables dropped.')


@contextmanager
def get_session() -> Session:
    """Context manager for database sessions with auto-commit/rollback."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def get_db():
    """Generator for FastAPI dependency injection."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
