from sqlmodel import Session, create_engine
from sqlmodel import SQLModel

# Database URL - Using SQLite for simplicity
DATABASE_URL = "sqlite:///./eleven.db"

# Create SQLModel engine
engine = create_engine(DATABASE_URL)

# Create tables
def create_db_and_tables():
    """Create all tables defined in SQLModel classes."""
    SQLModel.metadata.create_all(engine)

# Session dependency
def get_session():
    """Provide a database session for dependency injection."""
    with Session(engine) as session:
        yield session