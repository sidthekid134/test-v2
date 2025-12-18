from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app.models.models import (
    Item,
    get_session,
    get_items,
    get_item,
    create_item,
    update_item,
    delete_item,
)

router = APIRouter(
    prefix="/items",
    tags=["items"],
    responses={404: {"description": "Item not found"}},
)

@router.get("/", response_model=List[Item])
async def read_items(session: Session = Depends(get_session)):
    """
    Get all items representing the "11" implementation.
    """
    items = get_items(session)
    return items

@router.get("/{item_id}", response_model=Item)
async def read_item(item_id: int, session: Session = Depends(get_session)):
    """
    Get a specific item by ID.
    """
    db_item = get_item(session, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.post("/", response_model=Item)
async def create_new_item(item: Item, session: Session = Depends(get_session)):
    """
    Create a new item with "11" value.
    """
    # Default value is "11" if not provided
    if not item.value:
        item.value = "11"
    return create_item(session, item)

@router.put("/{item_id}", response_model=Item)
async def update_existing_item(item_id: int, item: Item, session: Session = Depends(get_session)):
    """
    Update an existing item.
    """
    db_item = update_item(session, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.delete("/{item_id}", response_model=Item)
async def delete_existing_item(item_id: int, session: Session = Depends(get_session)):
    """
    Delete an item.
    """
    db_item = delete_item(session, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

@router.post("/eleven", response_model=Item)
async def create_eleven(session: Session = Depends(get_session)):
    """
    Special endpoint to create an item with value "11".
    """
    item = Item(value="11", description="Created through the special eleven endpoint")
    return create_item(session, item)