from sqlmodel import Field, SQLModel
from typing import Optional


class Eleven(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    value: int = Field(default=11)
    description: Optional[str] = Field(default="This is the number 11")