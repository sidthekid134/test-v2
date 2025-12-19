from sqlmodel import Session, SQLModel, create_engine
import os
from typing import Generator

# Get database URL from environment variable or use default SQLite URL
DATABASE_URL = os.environ.get("DATABASE_URL") or "sqlite:///./eleven.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    echo=True,  # Log SQL queries for debugging
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

def create_db_and_tables():
    """Create database tables on startup."""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Dependency for getting DB session."""
    with Session(engine) as session:
        yield session