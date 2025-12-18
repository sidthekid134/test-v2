from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class TwelveBase(SQLModel):
    title: str
    description: Optional[str] = None
    is_completed: bool = False
    
class Twelve(TwelveBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
class TwelveCreate(TwelveBase):
    pass

class TwelveRead(TwelveBase):
    id: int
    created_at: datetime
    
class TwelveUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    is_completed: Optional[bool] = None