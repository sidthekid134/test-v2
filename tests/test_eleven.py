import pytest
from fastapi.testclient import TestClient

from main import app
from app.utils.eleven import get_eleven, is_eleven, elevens

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "11"}

def test_eleven_value_endpoint():
    response = client.get("/eleven/value")
    assert response.status_code == 200
    assert response.json() == 11

def test_check_if_eleven():
    response = client.get("/eleven/check/11")
    assert response.status_code == 200
    assert response.json() == {"value": 11, "is_eleven": True}
    
    response = client.get("/eleven/check/10")
    assert response.status_code == 200
    assert response.json() == {"value": 10, "is_eleven": False}

def test_get_eleven_list():
    response = client.get("/eleven/list?count=3")
    assert response.status_code == 200
    assert response.json() == [11, 11, 11]

def test_get_eleven_function():
    assert get_eleven() == 11

def test_is_eleven_function():
    assert is_eleven(11) is True
    assert is_eleven(10) is False
    assert is_eleven("11") is False

def test_elevens_function():
    assert elevens(3) == [11, 11, 11]
    assert len(elevens(5)) == 5
    assert all(x == 11 for x in elevens(10))