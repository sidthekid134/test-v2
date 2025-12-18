from sqlmodel import SQLModel, create_engine, Session

# SQLite database URL
SQLITE_DATABASE_URL = "sqlite:///./eleven.db"

# Create engine
engine = create_engine(
    SQLITE_DATABASE_URL, 
    echo=True,
    connect_args={"check_same_thread": False}  # Needed for SQLite
)

def create_db_and_tables():
    """Create database and tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """Get database session."""
    with Session(engine) as session:
        yield session