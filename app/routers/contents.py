from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from sqlmodel import select, Session, delete
from  ..database import get_session
from ..models.content import Content
from typing import Annotated
from datetime import datetime, timezone, timedelta
from ..utils.hashing import Hasher

#from ..dependencies import get_token_header

router = APIRouter(
    prefix="/contents",
    tags=["contents"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=list[Content])
async def get_contents(db: Session = Depends(get_session)):
    data = db.exec(select(Content)).unique()
    return data


@router.get("/{content_id}",response_model=Content)
async def get_content(content_id: int, db: Session = Depends(get_session)):
    data = db.get(Content, content_id)
    if not data:
        raise HTTPException(status_code=404, detail="Az adott tartalom nem található")
    return data


@router.delete("/{content_id}")
def delete_content(content_id: int,  db: Session = Depends(get_session)):
    content = db.get(Content, content_id)
    if not content:
        raise HTTPException(status_code=404, detail="Az adott tartalom nem található")
    db.delete(content)
    db.commit()
    return {"ok": True}

@router.put("/{content_id}", response_model=Content)
def update_content(content_id: int, content: Content, db: Session = Depends(get_session)):
    db_content = db.get(Content, content_id)
    if not db_content:
        raise HTTPException(status_code=404, detail="Az adott tartalom nem található")
    db_content.sqlmodel_update(content)
    db.add(db_content)
    db.commit()
    db.refresh(db_content)
    return db_content
