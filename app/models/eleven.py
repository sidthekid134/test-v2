from sqlmodel import Field, SQLModel
from typing import Optional
from datetime import datetime

class Eleven(SQLModel, table=True):
    """
    Eleven model that efficiently implements "11".
    
    Attributes:
        id: Primary key
        value: Always stores the value 11
        description: Optional description
        created_at: Timestamp when the record was created
    """
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int = Field(default=11, index=True)
    description: Optional[str] = Field(default="Efficient implementation of 11")
    created_at: datetime = Field(default_factory=datetime.utcnow)