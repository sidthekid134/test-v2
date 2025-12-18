from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.models.story import Story
from app.config.database import get_session

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
    responses={404: {"description": "Not found"}},
)

class StoryCreate(Story):
    pass

class StoryRead(Story):
    pass

class StoryUpdate(Story):
    title: str = None
    description: str = None
    status: str = None

@router.get("/", response_model=List[StoryRead])
def get_stories(session: Session = Depends(get_session)):
    """Get all stories"""
    stories = session.exec(select(Story)).all()
    return stories

@router.get("/{story_id}", response_model=StoryRead)
def get_story(story_id: int, session: Session = Depends(get_session)):
    """Get a specific story by ID"""
    story = session.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    return story

@router.post("/", response_model=StoryRead)
def create_story(story: StoryCreate, session: Session = Depends(get_session)):
    """Create a new story"""
    db_story = Story.from_orm(story)
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story

@router.patch("/{story_id}", response_model=StoryRead)
def update_story(story_id: int, story: StoryUpdate, session: Session = Depends(get_session)):
    """Update a story"""
    db_story = session.get(Story, story_id)
    if not db_story:
        raise HTTPException(status_code=404, detail="Story not found")
    
    story_data = story.dict(exclude_unset=True)
    for key, value in story_data.items():
        setattr(db_story, key, value)
    
    db_story.updated_at = datetime.utcnow()
    session.add(db_story)
    session.commit()
    session.refresh(db_story)
    return db_story

@router.delete("/{story_id}")
def delete_story(story_id: int, session: Session = Depends(get_session)):
    """Delete a story"""
    story = session.get(Story, story_id)
    if not story:
        raise HTTPException(status_code=404, detail="Story not found")
    session.delete(story)
    session.commit()
    return {"ok": True}