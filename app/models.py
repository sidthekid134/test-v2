from sqlmodel import Field, SQLModel
from typing import Optional

class Eleven(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int = Field(default=11)
    
class Twelve(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int = Field(default=12)