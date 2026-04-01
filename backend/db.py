import os
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy import text
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL, echo=False) if DATABASE_URL else None


def get_session():
    """Yield a database session for dependency injection."""
    if engine is None:
        raise RuntimeError("DATABASE_URL is not configured")
    with Session(engine) as session:
        yield session


def check_database_connection() -> tuple[bool, str]:
    """Check if database connection is working.

    Returns:
        Tuple of (is_connected, message)
    """
    if engine is None:
        return False, "error: DATABASE_URL not configured"
    try:
        with Session(engine) as session:
            session.exec(text("SELECT 1"))
        return True, "connected"
    except Exception as e:
        return False, f"error: {str(e)}"


def create_db_and_tables():
    """Create all database tables."""
    if engine is None:
        raise RuntimeError("DATABASE_URL is not configured")
    SQLModel.metadata.create_all(engine)
