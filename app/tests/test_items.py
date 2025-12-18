import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.models.models import Item
from main import app

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session

    app.dependency_overrides = {}
    from app.models.models import get_session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_create_item(client: TestClient):
    response = client.post(
        "/items/", json={"value": "11", "description": "Test item"}
    )
    data = response.json()
    assert response.status_code == 200
    assert data["value"] == "11"
    assert data["description"] == "Test item"
    assert data["id"] is not None

def test_create_eleven(client: TestClient):
    response = client.post("/items/eleven")
    data = response.json()
    assert response.status_code == 200
    assert data["value"] == "11"
    assert "Created through the special eleven endpoint" in data["description"]
    assert data["id"] is not None

def test_read_items(client: TestClient):
    # Create a test item first
    client.post("/items/", json={"value": "11"})
    
    response = client.get("/items/")
    data = response.json()
    assert response.status_code == 200
    assert len(data) > 0
    assert data[0]["value"] == "11"

def test_read_item(client: TestClient):
    # Create a test item first
    create_response = client.post("/items/", json={"value": "11"})
    created_item = create_response.json()
    
    response = client.get(f"/items/{created_item['id']}")
    data = response.json()
    assert response.status_code == 200
    assert data["value"] == "11"
    assert data["id"] == created_item["id"]