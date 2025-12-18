from sqlmodel import Field, SQLModel, Relationship
from typing import Optional, List
from datetime import datetime

class ItemBase(SQLModel):
    """Base model for Item."""
    
    name: str
    description: Optional[str] = None
    price: float
    
class Item(ItemBase, table=True):
    """Item database model."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
class ItemCreate(ItemBase):
    """Model for creating an item."""
    
    pass
    
class ItemRead(ItemBase):
    """Model for reading item information."""
    
    id: int
    user_id: Optional[int]
    created_at: datetime