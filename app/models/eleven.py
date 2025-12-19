from typing import Optional, List, Dict, Union
from sqlmodel import Field, SQLModel
from datetime import datetime
from enum import Enum

class ElevenType(str, Enum):
    """Types of eleven representations."""
    NUMERIC = "numeric"
    BINARY = "binary"
    HEX = "hex"
    ROMAN = "roman"
    STRING = "string"
    SEQUENCE = "sequence"
    CUSTOM = "custom"

class ElevenBase(SQLModel):
    """Base model for eleven-related data."""
    value: int = Field(default=11)
    description: Optional[str] = Field(default=None)
    type: ElevenType = Field(default=ElevenType.NUMERIC)
    properties: Optional[Dict[str, Union[str, int, List[int]]]] = Field(default=None)
    
class Eleven(ElevenBase, table=True):
    """Eleven entity in the database."""
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    def is_valid(self) -> bool:
        """Check if the entity represents a valid eleven."""
        if self.type == ElevenType.NUMERIC:
            return self.value == 11
        elif self.type == ElevenType.BINARY:
            return self.properties and self.properties.get("binary") == "0b1011"
        elif self.type == ElevenType.HEX:
            return self.properties and self.properties.get("hex") == "0xB"
        elif self.type == ElevenType.ROMAN:
            return self.properties and self.properties.get("roman") == "XI"
        elif self.type == ElevenType.STRING:
            return self.properties and self.properties.get("string") == "11"
        elif self.type == ElevenType.SEQUENCE:
            return self.properties and self.properties.get("sequence") == [1, 1]
        elif self.type == ElevenType.CUSTOM:
            # For custom type, just check if value equals 11
            return self.value == 11
        return False

class ElevenCreate(ElevenBase):
    """Schema for creating a new eleven entity."""
    pass

class ElevenRead(ElevenBase):
    """Schema for reading an eleven entity."""
    id: int
    created_at: datetime
    updated_at: datetime

class ElevenUpdate(SQLModel):
    """Schema for updating an eleven entity."""
    description: Optional[str] = None
    properties: Optional[Dict[str, Union[str, int, List[int]]]] = None