from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class ItemBase(SQLModel):
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True

class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class ItemCreate(ItemBase):
    pass

class ItemRead(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime

class ItemUpdate(SQLModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None