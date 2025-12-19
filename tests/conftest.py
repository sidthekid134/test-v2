import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session, create_engine
from sqlmodel.pool import StaticPool

from app.config.database import get_session
from main import app

@pytest.fixture(name="test_client")
def test_client_fixture():
    """Create test client for FastAPI app."""
    client = TestClient(app)
    return client

@pytest.fixture(name="test_db_session")
def test_db_session_fixture():
    """Create test database session with in-memory SQLite database."""
    # Create in-memory SQLite test database
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    # Create tables
    SQLModel.metadata.create_all(test_engine)

    # Override get_session dependency
    def get_test_session():
        with Session(test_engine) as session:
            yield session
    
    app.dependency_overrides[get_session] = get_test_session
    
    # Create a new session for testing
    with Session(test_engine) as session:
        yield session
    
    # Clear dependency override
    app.dependency_overrides.clear()