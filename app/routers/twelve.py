from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List

from ..models import Twelve
from ..database import get_session
from ..utils.twelve import get_twelve, is_twelve, twelves

router = APIRouter(
    prefix="/twelve",
    tags=["twelve"],
)

@router.get("/", response_model=List[Twelve])
def get_twelves(session: Session = Depends(get_session)):
    twelves = session.exec(select(Twelve)).all()
    return twelves

@router.post("/", response_model=Twelve)
def create_twelve(session: Session = Depends(get_session)):
    twelve = Twelve(value=12)
    session.add(twelve)
    session.commit()
    session.refresh(twelve)
    return twelve

@router.get("/value")
def get_twelve_value():
    return get_twelve()

@router.get("/check/{value}")
def check_if_twelve(value: int):
    return {"value": value, "is_twelve": is_twelve(value)}

@router.get("/list")
def get_twelve_list(count: int = Query(1, ge=1, le=100)):
    return twelves(count)