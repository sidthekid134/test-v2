from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the 11 API"}


def test_eleven_value():
    response = client.get("/eleven/value")
    assert response.status_code == 200
    assert response.json() == {"value": 11}