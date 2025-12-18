import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from main import app
from app.config.database import get_session
from app.models.eleven import Eleven
from app.models.story import Story

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
    assert response.json() == {"message": "Story API with Eleven implementation"}

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

def test_create_story(client, session):
    # Test creating a new story
    story_data = {
        "title": "Test Story",
        "description": "This is a test story"
    }
    response = client.post("/stories/", json=story_data)
    assert response.status_code == 200
    
    data = response.json()
    assert data["title"] == "Test Story"
    assert data["description"] == "This is a test story"
    assert data["status"] == "new"
    assert data["id"] is not None
    
    # Check if created in DB
    story = session.get(Story, data["id"])
    assert story is not None
    assert story.title == "Test Story"
    assert story.description == "This is a test story"

def test_get_stories(client, session):
    # Create a few Story objects
    for i in range(3):
        story = Story(title=f"Test Story {i}", description=f"Description {i}")
        session.add(story)
    session.commit()
    
    response = client.get("/stories/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 3
    assert any(item["title"] == "Test Story 1" for item in data)

def test_get_story(client, session):
    # Create a story
    story = Story(title="Test Story", description="Test Description")
    session.add(story)
    session.commit()
    session.refresh(story)
    
    response = client.get(f"/stories/{story.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Story"
    assert data["description"] == "Test Description"
    
    # Test non-existent story
    response = client.get("/stories/9999")
    assert response.status_code == 404

def test_update_story(client, session):
    # Create a story
    story = Story(title="Original Title", description="Original Description")
    session.add(story)
    session.commit()
    session.refresh(story)
    
    # Update the story
    update_data = {
        "title": "Updated Title",
        "status": "in-progress"
    }
    response = client.patch(f"/stories/{story.id}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["description"] == "Original Description"  # Unchanged
    assert data["status"] == "in-progress"
    
    # Verify in DB
    updated_story = session.get(Story, story.id)
    assert updated_story.title == "Updated Title"
    assert updated_story.status == "in-progress"
    assert updated_story.updated_at is not None

def test_delete_story(client, session):
    # Create a story
    story = Story(title="Story to Delete", description="Will be deleted")
    session.add(story)
    session.commit()
    session.refresh(story)
    story_id = story.id
    
    # Delete the story
    response = client.delete(f"/stories/{story_id}")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
    
    # Verify it's gone from DB
    deleted_story = session.get(Story, story_id)
    assert deleted_story is None
    
    # Try to delete non-existent story
    response = client.delete("/stories/9999")
    assert response.status_code == 404