from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class UserBase(SQLModel):
    """Base model for User."""
    
    username: str = Field(index=True)
    email: str = Field(index=True)
    is_active: bool = True
    
class User(UserBase, table=True):
    """User database model."""
    
    id: Optional[int] = Field(default=None, primary_key=True)
    password: str
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
class UserCreate(UserBase):
    """Model for creating a user."""
    
    password: str
    
class UserRead(UserBase):
    """Model for reading user information."""
    
    id: int
    created_at: datetime