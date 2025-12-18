from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class ItemBase(SQLModel):
    """Base Item model with shared attributes"""
    name: str
    description: Optional[str] = None
    price: float
    is_available: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class Item(ItemBase, table=True):
    """Item DB model for storing in the database"""
    id: Optional[int] = Field(default=None, primary_key=True)
    
class ItemCreate(ItemBase):
    """Item schema for creation"""
    pass

class ItemResponse(ItemBase):
    """Item response schema"""
    id: int
    
class ItemUpdate(SQLModel):
    """Item schema for updates"""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    is_available: Optional[bool] = None