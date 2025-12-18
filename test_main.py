import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from app.config.database import get_session
from app.models.eleven import Eleven

@pytest.fixture(name="session")
def session_fixture():
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
    def get_session_override():
        yield session

    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Implementation of 11"}

def test_eleven_endpoint(client):
    response = client.get("/11")
    assert response.status_code == 200
    assert response.json() == {"value": 11}

def test_create_eleven(client, session):
    response = client.post("/eleven/")
    assert response.status_code == 200
    data = response.json()
    assert data["value"] == 11
    assert data["id"] is not None
    
    # Check if created in DB
    eleven = session.get(Eleven, data["id"])
    assert eleven is not None
    assert eleven.value == 11

def test_get_elevens(client, session):
    # Create a few Eleven objects
    for _ in range(3):
        eleven = Eleven()
        session.add(eleven)
    session.commit()
    
    response = client.get("/eleven/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert all(item["value"] == 11 for item in data)