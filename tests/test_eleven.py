from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.models.eleven import Eleven
from main import app

# Create a test client
client = TestClient(app)

# Test in-memory database
TEST_DATABASE_URL = "sqlite://"
engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

def test_read_main():
    """Test the root endpoint."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "eleven" in data

def test_get_eleven_direct():
    """Test the /11 endpoint."""
    response = client.get("/11")
    assert response.status_code == 200
    data = response.json()
    assert data == {"value": 11}

def test_get_eleven_router():
    """Test the /eleven endpoint from the router."""
    response = client.get("/eleven")
    assert response.status_code == 200
    data = response.json()
    assert data == {"value": 11}