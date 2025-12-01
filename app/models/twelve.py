from sqlmodel import Field, SQLModel
from typing import Optional


class Twelve(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int = Field(default=12)
    description: Optional[str] = Field(default="This is the number 12")