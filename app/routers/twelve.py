from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.models.twelve import Twelve
from app.database import get_session

router = APIRouter(
    prefix="/twelve",
    tags=["twelve"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Twelve])
def get_twelves(session: Session = Depends(get_session)):
    """Get all twelve records"""
    twelves = session.exec(select(Twelve)).all()
    return twelves


@router.get("/value")
def get_twelve_value():
    """Get the value 12"""
    return {"value": 12}


@router.get("/{twelve_id}", response_model=Twelve)
def get_twelve(twelve_id: int, session: Session = Depends(get_session)):
    """Get a specific twelve record by ID"""
    twelve = session.get(Twelve, twelve_id)
    if not twelve:
        raise HTTPException(status_code=404, detail="Twelve not found")
    return twelve


@router.post("/", response_model=Twelve)
def create_twelve(session: Session = Depends(get_session)):
    """Create a new twelve record"""
    twelve = Twelve()
    session.add(twelve)
    session.commit()
    session.refresh(twelve)
    return twelve