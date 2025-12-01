from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List

from ..models import Eleven
from ..database import get_session
from ..utils.eleven import get_eleven, is_eleven, elevens

router = APIRouter(
    prefix="/eleven",
    tags=["eleven"],
)

@router.get("/", response_model=List[Eleven])
def get_elevens(session: Session = Depends(get_session)):
    elevens = session.exec(select(Eleven)).all()
    return elevens

@router.post("/", response_model=Eleven)
def create_eleven(session: Session = Depends(get_session)):
    eleven = Eleven(value=11)
    session.add(eleven)
    session.commit()
    session.refresh(eleven)
    return eleven

@router.get("/value")
def get_eleven_value():
    return get_eleven()

@router.get("/check/{value}")
def check_if_eleven(value: int):
    return {"value": value, "is_eleven": is_eleven(value)}

@router.get("/list")
def get_eleven_list(count: int = Query(1, ge=1, le=100)):
    return elevens(count)