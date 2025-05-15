from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from sqlmodel import select, Session, delete
from  ..database import get_session
from ..models.ingatlanok import Ingatlan,IngatlanPublic
from typing import Annotated
from datetime import datetime, timezone, timedelta
from ..utils.hashing import Hasher

#from ..dependencies import get_token_header

router = APIRouter(
    prefix="/api/ingatlan",
    tags=["ingatlan"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=list[IngatlanPublic])
async def get_ingatlan(db: Session = Depends(get_session)):
    data = db.exec(select(Ingatlan)).unique()
    return data


@router.get("/{ingatlan_id}",response_model=IngatlanPublic)
async def get_ingatlan(ingatlan_id: int, db: Session = Depends(get_session)):
    data = db.get(Ingatlan, ingatlan_id)
    if not data:
        raise HTTPException(status_code=404, detail="Az adott tartalom nem található")
    return data


@router.delete("/{ingatlan_id}",status_code=204)
def delete_ingatlan(ingatlan_id: int,  db: Session = Depends(get_session)):
    ingatlan = db.get(Ingatlan, ingatlan_id)
    if not ingatlan:
        raise HTTPException(status_code=404, detail="Az adott tartalom nem található")
    db.delete(ingatlan)
    db.commit()
    return {"ok": True}

@router.put("/{ingatlan_id}", response_model=Ingatlan)
def update_ingatlan(ingatlan_id: int, ingatlan: Ingatlan, db: Session = Depends(get_session)):
    db_ingatlan = db.get(Ingatlan, ingatlan_id)
    if not db_ingatlan:
        raise HTTPException(status_code=404, detail="Az adott tartalom nem található")
    db_ingatlan.sqlmodel_update(ingatlan)
    db.add(db_ingatlan)
    db.commit()
    db.refresh(db_ingatlan)
    return db_ingatlan

@router.post("/", response_model=Ingatlan,status_code=201)
def add_ingatlan(ingatlan: Ingatlan, db: Session = Depends(get_session)):
    db.add(ingatlan)
    db.commit()
    db.refresh(ingatlan)
    return ingatlan