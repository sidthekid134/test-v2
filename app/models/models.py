from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class ItemBase(SQLModel):
    """Base model for items."""
    name: str
    description: Optional[str] = None
    value: int = 11  # Default value of 11

class Item(ItemBase, table=True):
    """Item model for the database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    
    # Relationships could be added here if needed
    # For example:
    # category_id: Optional[int] = Field(default=None, foreign_key="category.id")
    # category: Optional["Category"] = Relationship(back_populates="items")

class ItemCreate(ItemBase):
    """Item model for creating items."""
    pass

class ItemRead(ItemBase):
    """Item model for reading items."""
    id: int