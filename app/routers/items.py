from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from datetime import datetime

from app.models.item import Item, ItemCreate, ItemRead
from app.database.db import get_session

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ItemRead)
def create_item(item: ItemCreate, user_id: int, session: Session = Depends(get_session)):
    """Create a new item."""
    db_item = Item.from_orm(item)
    db_item.user_id = user_id
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ItemRead])
def read_items(skip: int = 0, limit: int = 100, session: Session = Depends(get_session)):
    """Get all items."""
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return items

@router.get("/{item_id}", response_model=ItemRead)
def read_item(item_id: int, session: Session = Depends(get_session)):
    """Get a specific item by ID."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=ItemRead)
def update_item(item_id: int, item: ItemCreate, session: Session = Depends(get_session)):
    """Update an item."""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    
    db_item.updated_at = datetime.utcnow()
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_item(item_id: int, session: Session = Depends(get_session)):
    """Delete an item."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(item)
    session.commit()
    return {"ok": True}