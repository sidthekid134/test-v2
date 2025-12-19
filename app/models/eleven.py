from typing import Optional, List, Dict, Any, Union
from sqlmodel import Field, SQLModel
from pydantic import validator
import math

class ElevenBase(SQLModel):
    """Base model for eleven-related data."""
    value: int = Field(default=11)
    description: Optional[str] = Field(default=None)
    metadata: Optional[Dict[str, Any]] = Field(default=None)
    is_prime: bool = Field(default=True)
    
    @validator("value")
    def validate_value(cls, v):
        """Ensure the value is related to 11 in some way."""
        if v != 11 and v % 11 != 0 and v != 1:
            raise ValueError("Value must be 11, a multiple of 11, or 1")
        return v
        
    @property
    def doubled(self) -> int:
        """Return the value doubled."""
        return self.value * 2
    
    @property
    def binary(self) -> str:
        """Return the binary representation of the value."""
        return bin(self.value)
    
    @property
    def properties(self) -> Dict[str, Any]:
        """Return mathematical properties related to the value."""
        return {
            "is_prime": self.is_prime,
            "binary": self.binary,
            "square": self.value ** 2,
            "square_root": math.sqrt(self.value),
            "reciprocal": 1 / self.value
        }
    
class Eleven(ElevenBase, table=True):
    """Eleven entity in the database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: Optional[str] = Field(default=None)
    updated_at: Optional[str] = Field(default=None)

class ElevenCreate(ElevenBase):
    """Schema for creating a new eleven entity."""
    pass

class ElevenRead(ElevenBase):
    """Schema for reading an eleven entity."""
    id: int

class ElevenUpdate(SQLModel):
    """Schema for updating an eleven entity."""
    value: Optional[int] = None
    description: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class ElevenResponse(ElevenRead):
    """Enhanced response schema with calculated fields."""
    properties: Dict[str, Any] = {}
    doubled: int = 22