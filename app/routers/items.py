from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List

from app.core.database import get_session
from app.models.item import Item, ItemCreate, ItemResponse, ItemUpdate

router = APIRouter(
    prefix="/items",
    tags=["items"],
)

@router.post("/", response_model=ItemResponse, status_code=status.HTTP_201_CREATED)
def create_item(*, session: Session = Depends(get_session), item: ItemCreate):
    """Create a new item"""
    db_item = Item.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ItemResponse])
def read_items(*, session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    """Get all items with pagination"""
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return items

@router.get("/{item_id}", response_model=ItemResponse)
def read_item(*, session: Session = Depends(get_session), item_id: int):
    """Get item by ID"""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.patch("/{item_id}", response_model=ItemResponse)
def update_item(*, session: Session = Depends(get_session), item_id: int, item: ItemUpdate):
    """Update an item"""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
    
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    """Delete an item"""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(item)
    session.commit()
    return None