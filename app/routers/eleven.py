from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List

from app.models.eleven import Eleven
from app.database import get_session

router = APIRouter(
    prefix="/eleven",
    tags=["eleven"],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[Eleven])
def get_elevens(session: Session = Depends(get_session)):
    """Get all eleven records"""
    elevens = session.exec(select(Eleven)).all()
    return elevens


@router.get("/value")
def get_eleven_value():
    """Get the value 11"""
    return {"value": 11}


@router.get("/{eleven_id}", response_model=Eleven)
def get_eleven(eleven_id: int, session: Session = Depends(get_session)):
    """Get a specific eleven record by ID"""
    eleven = session.get(Eleven, eleven_id)
    if not eleven:
        raise HTTPException(status_code=404, detail="Eleven not found")
    return eleven


@router.post("/", response_model=Eleven)
def create_eleven(session: Session = Depends(get_session)):
    """Create a new eleven record"""
    eleven = Eleven()
    session.add(eleven)
    session.commit()
    session.refresh(eleven)
    return eleven