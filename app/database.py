from sqlmodel import Session, SQLModel, create_engine
import os

# Create SQLite database URL
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./eleven_twelve.db")

# Create SQLite engine
engine = create_engine(
    DATABASE_URL, 
    connect_args={"check_same_thread": False},
    echo=True
)


def create_db_and_tables():
    """Create database and tables on startup"""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session