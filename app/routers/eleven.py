from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.config.database import get_session
from app.models.eleven import Eleven, ElevenCreate, ElevenRead

router = APIRouter(
    prefix="/eleven",
    tags=["eleven"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=List[ElevenRead])
def get_all_elevens(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session)
):
    """Get all eleven entities."""
    elevens = session.exec(select(Eleven).offset(skip).limit(limit)).all()
    return elevens

@router.post("/", response_model=ElevenRead, status_code=status.HTTP_201_CREATED)
def create_eleven(
    eleven: ElevenCreate, 
    session: Session = Depends(get_session)
):
    """Create a new eleven entity."""
    db_eleven = Eleven.from_orm(eleven)
    session.add(db_eleven)
    session.commit()
    session.refresh(db_eleven)
    return db_eleven

@router.get("/{eleven_id}", response_model=ElevenRead)
def get_eleven(
    eleven_id: int, 
    session: Session = Depends(get_session)
):
    """Get a specific eleven entity by ID."""
    eleven = session.get(Eleven, eleven_id)
    if not eleven:
        raise HTTPException(status_code=404, detail="Eleven not found")
    return eleven

@router.get("/value", response_model=dict)
def get_eleven_value():
    """Get the constant value 11."""
    return {"value": 11}

@router.get("/pattern", response_model=dict)
def get_eleven_pattern():
    """Get various patterns of 11."""
    return {
        "numeric": 11,
        "string": "11",
        "binary": "0b1011",
        "octal": "0o13",
        "hex": "0xB",
        "roman": "XI",
        "pattern": [1, 1],
        "calculated": "5 + 6 = 11"
    }