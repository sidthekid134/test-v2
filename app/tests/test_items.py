from fastapi.testclient import TestClient
import pytest
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from app.models.models import Item
from app.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    """Create an in-memory SQLite database for testing."""
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session):
    """Create a test client with the test database session."""
    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_item(client):
    """Test creating an item."""
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "Test Description", "value": 11},
    )
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["value"] == 11
    assert "id" in data

def test_read_items(client, session):
    """Test reading items."""
    # Create test items
    item1 = Item(name="Test Item 1", value=11)
    item2 = Item(name="Test Item 2", value=11)
    session.add(item1)
    session.add(item2)
    session.commit()

    response = client.get("/items/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2
    assert data[0]["name"] == "Test Item 1"
    assert data[1]["name"] == "Test Item 2"

def test_read_eleven_items(client, session):
    """Test reading items with value=11."""
    # Create test items
    item1 = Item(name="Test Item 1", value=11)
    item2 = Item(name="Test Item 2", value=11)
    item3 = Item(name="Test Item 3", value=22)  # Different value
    session.add(item1)
    session.add(item2)
    session.add(item3)
    session.commit()

    response = client.get("/items/eleven")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2  # Only items with value=11
    assert all(item["value"] == 11 for item in data)