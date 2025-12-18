from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List, Dict, Any

from app.database import get_session
from app.models.eleven import Eleven

router = APIRouter(
    prefix="/eleven",
    tags=["eleven"],
    responses={404: {"description": "Not found"}},
)

@router.get("/", response_model=Dict[str, int])
def get_eleven():
    """
    Returns the number 11.
    
    This is the most efficient implementation of "11" possible.
    """
    return {"value": 11}

@router.get("/db", response_model=List[Eleven])
def get_eleven_from_db(*, session: Session = Depends(get_session)):
    """
    Returns all Eleven objects from the database.
    
    If none exist, creates one with the value 11.
    """
    elevens = session.exec(select(Eleven)).all()
    if not elevens:
        eleven = Eleven()
        session.add(eleven)
        session.commit()
        session.refresh(eleven)
        elevens = [eleven]
    return elevens

@router.post("/", response_model=Eleven)
def create_eleven(*, session: Session = Depends(get_session), description: str = None):
    """
    Creates a new Eleven object in the database.
    
    The value is always 11, but the description can be customized.
    """
    eleven = Eleven()
    if description:
        eleven.description = description
    session.add(eleven)
    session.commit()
    session.refresh(eleven)
    return eleven