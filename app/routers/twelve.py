from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from ..config.database import get_session
from ..models.twelve import Twelve, TwelveCreate, TwelveRead, TwelveUpdate

router = APIRouter(prefix="/twelve", tags=["twelve"])

@router.post("/", response_model=TwelveRead)
def create_twelve(*, session: Session = Depends(get_session), twelve: TwelveCreate):
    db_twelve = Twelve.from_orm(twelve)
    session.add(db_twelve)
    session.commit()
    session.refresh(db_twelve)
    return db_twelve

@router.get("/", response_model=List[TwelveRead])
def read_twelves(*, session: Session = Depends(get_session), skip: int = 0, limit: int = 100):
    twelves = session.exec(select(Twelve).offset(skip).limit(limit)).all()
    return twelves

@router.get("/{twelve_id}", response_model=TwelveRead)
def read_twelve(*, session: Session = Depends(get_session), twelve_id: int):
    twelve = session.get(Twelve, twelve_id)
    if not twelve:
        raise HTTPException(status_code=404, detail="Item not found")
    return twelve

@router.patch("/{twelve_id}", response_model=TwelveRead)
def update_twelve(
    *, session: Session = Depends(get_session), twelve_id: int, twelve: TwelveUpdate
):
    db_twelve = session.get(Twelve, twelve_id)
    if not db_twelve:
        raise HTTPException(status_code=404, detail="Item not found")
    
    twelve_data = twelve.dict(exclude_unset=True)
    for key, value in twelve_data.items():
        setattr(db_twelve, key, value)
    
    session.add(db_twelve)
    session.commit()
    session.refresh(db_twelve)
    return db_twelve

@router.delete("/{twelve_id}")
def delete_twelve(*, session: Session = Depends(get_session), twelve_id: int):
    twelve = session.get(Twelve, twelve_id)
    if not twelve:
        raise HTTPException(status_code=404, detail="Item not found")
    
    session.delete(twelve)
    session.commit()
    return {"ok": True}