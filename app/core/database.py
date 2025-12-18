from sqlmodel import SQLModel, Session, create_engine
import os
from typing import Generator

# Database URL - using SQLite for simplicity
DATABASE_URL = "sqlite:///./test.db"

# Create engine
engine = create_engine(DATABASE_URL, echo=True, connect_args={"check_same_thread": False})

def create_db_and_tables():
    """Create database tables from SQLModel metadata"""
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    """Database session dependency"""
    with Session(engine) as session:
        yield session