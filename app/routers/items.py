from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from datetime import datetime

from app.models.models import Item, ItemCreate, ItemRead, ItemUpdate
from app.config.database import get_session

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=ItemRead)
def create_item(*, session: Session = Depends(get_session), item: ItemCreate):
    db_item = Item.from_orm(item)
    session.add(db_item)
    session.commit()
    session.refresh(db_item)
    return db_item

@router.get("/", response_model=List[ItemRead])
def read_items(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, lte=100),
    name: Optional[str] = None,
    is_available: Optional[bool] = None
):
    query = select(Item)
    
    if name:
        query = query.where(Item.name.contains(name))
    
    if is_available is not None:
        query = query.where(Item.is_available == is_available)
    
    items = session.exec(query.offset(offset).limit(limit)).all()
    return items

@router.get("/{item_id}", response_model=ItemRead)
def read_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.patch("/{item_id}", response_model=ItemRead)
def update_item(
    *, session: Session = Depends(get_session), item_id: int, item: ItemUpdate
):
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
def delete_item(*, session: Session = Depends(get_session), item_id: int):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(item)
    session.commit()
    return {"ok": True}