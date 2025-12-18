from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.database import get_session
from app.models.models import Item, ItemCreate, ItemRead

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}},
)

@router.post("/", response_model=ItemRead)
def create_item(*, session: Session = Depends(get_session), item: ItemCreate):
    """Create a new item."""
    db_item = Item.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ItemRead])
def read_items(*, session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    """Read all items."""
    items = session.exec(select(Item).offset(skip).limit(limit)).all()
    return items

@router.get("/eleven", response_model=List[ItemRead])
def read_eleven_items(*, session: Session = Depends(get_session)):
    """Read all items with value exactly 11."""
    items = session.exec(select(Item).where(Item.value == 11)).all()
    return items

@router.get("/{item_id}", response_model=ItemRead)
def read_item(*, session: Session = Depends(get_session), item_id: int):
    """Read a specific item by ID."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.patch("/{item_id}", response_model=ItemRead)
def update_item(*, session: Session = Depends(get_session), item_id: int, item: ItemCreate):
    """Update a specific item by ID."""
    db_item = session.get(Item, item_id)
    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Update model attributes
    item_data = item.dict(exclude_unset=True)
    for key, value in item_data.items():
        setattr(db_item, key, value)
        
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.delete("/{item_id}")
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    """Delete a specific item by ID."""
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(item)
    session.commit()
    return {"ok": True}