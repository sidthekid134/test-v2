import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.models.eleven import Eleven, ElevenCreate

def test_root_endpoint(test_client: TestClient):
    """Test the root endpoint."""
    response = test_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the 11 API"}

def test_get_eleven_value(test_client: TestClient):
    """Test the /eleven/value endpoint."""
    response = test_client.get("/eleven/value")
    assert response.status_code == 200
    assert response.json() == {"value": 11}

def test_get_eleven_pattern(test_client: TestClient):
    """Test the /eleven/pattern endpoint."""
    response = test_client.get("/eleven/pattern")
    assert response.status_code == 200
    data = response.json()
    assert data["numeric"] == 11
    assert data["string"] == "11"
    assert data["pattern"] == [1, 1]

def test_create_eleven(test_client: TestClient, test_db_session: Session):
    """Test creating an eleven entity."""
    # Create a new eleven entity
    eleven_data = {
        "value": 11,
        "description": "Test Eleven"
    }
    response = test_client.post("/eleven/", json=eleven_data)
    assert response.status_code == 201
    data = response.json()
    assert data["value"] == 11
    assert data["description"] == "Test Eleven"
    assert "id" in data
    
    # Check that it was actually saved to the database
    db_eleven = test_db_session.get(Eleven, data["id"])
    assert db_eleven is not None
    assert db_eleven.value == 11
    assert db_eleven.description == "Test Eleven"

def test_get_all_elevens(test_client: TestClient, test_db_session: Session):
    """Test getting all eleven entities."""
    # Create some test data
    eleven1 = Eleven(value=11, description="First Eleven")
    eleven2 = Eleven(value=11, description="Second Eleven")
    test_db_session.add(eleven1)
    test_db_session.add(eleven2)
    test_db_session.commit()
    
    # Get all elevens
    response = test_client.get("/eleven/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    
    # Verify the data
    descriptions = [item["description"] for item in data]
    assert "First Eleven" in descriptions
    assert "Second Eleven" in descriptions