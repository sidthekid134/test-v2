import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.models.models import Item
from main import app

@pytest.fixture(name="client")
def client_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    
    def get_session_override():
        with Session(engine) as session:
            yield session
    
    from app.config.database import get_session
    app.dependency_overrides[get_session] = get_session_override
    
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_item(client):
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "Test Description", "price": 10.99},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["price"] == 10.99
    assert data["is_available"] is True
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data

def test_read_item(client):
    # First create an item
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "Test Description", "price": 10.99},
    )
    data = response.json()
    item_id = data["id"]
    
    # Then read it
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "Test Description"
    assert data["price"] == 10.99
    assert data["id"] == item_id

def test_update_item(client):
    # First create an item
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "Test Description", "price": 10.99},
    )
    data = response.json()
    item_id = data["id"]
    
    # Then update it
    response = client.patch(
        f"/items/{item_id}",
        json={"name": "Updated Item", "price": 19.99},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Item"
    assert data["description"] == "Test Description"  # Unchanged
    assert data["price"] == 19.99
    assert data["id"] == item_id

def test_delete_item(client):
    # First create an item
    response = client.post(
        "/items/",
        json={"name": "Test Item", "description": "Test Description", "price": 10.99},
    )
    data = response.json()
    item_id = data["id"]
    
    # Then delete it
    response = client.delete(f"/items/{item_id}")
    assert response.status_code == 200
    
    # Verify it's deleted
    response = client.get(f"/items/{item_id}")
    assert response.status_code == 404