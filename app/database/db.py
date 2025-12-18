from sqlmodel import Session, SQLModel, create_engine
import os
from pathlib import Path

# Define database URL - using SQLite for simplicity
DATABASE_URL = "sqlite:///./11.db"

# Create engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True  # Set to False in production
)

def create_db_and_tables():
    """Create database and tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session