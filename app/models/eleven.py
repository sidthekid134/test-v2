from typing import Optional
from sqlmodel import Field, SQLModel

class ElevenBase(SQLModel):
    """Base model for eleven-related data."""
    value: int = Field(default=11)
    description: Optional[str] = Field(default=None)
    
class Eleven(ElevenBase, table=True):
    """Eleven entity in the database."""
    id: Optional[int] = Field(default=None, primary_key=True)

class ElevenCreate(ElevenBase):
    """Schema for creating a new eleven entity."""
    pass

class ElevenRead(ElevenBase):
    """Schema for reading an eleven entity."""
    id: int