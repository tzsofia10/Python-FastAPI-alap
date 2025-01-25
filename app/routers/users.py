from fastapi import APIRouter, Depends, HTTPException, status, Cookie
from sqlmodel import select, Session, delete
from  ..database import get_session
from ..models.user import User, UserPublic, UserCreate, UserUpdate
from ..utils.auth import Token, LoginData, authenticate_user, get_current_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES
from typing import Annotated
from datetime import datetime, timezone, timedelta
from ..utils.hashing import Hasher

#from ..dependencies import get_token_header

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)

@router.get("/",response_model=list[UserPublic])
async def get_userek(db: Session = Depends(get_session)):
    data = db.exec(select(User)).unique()
    return data

@router.get("/me", response_model=UserPublic)
async def user_en(
    current_user: Annotated[User, Depends(get_current_user)],
):
    return current_user

@router.get("/{user_id}",response_model=UserPublic)
async def get_user(user_id: int, db: Session = Depends(get_session)):
    data = db.get(User, user_id)
    if not data:
        raise HTTPException(status_code=404, detail="Az adott felhasználó nem található")
    return data


@router.delete("/{user_id}")
def delete_user(user_id: int,  db: Session = Depends(get_session)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Az adott felhasználó nem található")
    db.delete(user)
    db.commit()
    return {"ok": True}

@router.put("/{user_id}", response_model=UserPublic)
def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_session)):
    db_user = db.get(User, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Az adott felhasználó nem található")
    user_data = User(
        id=user_id,
        password_hash=db_user.password_hash
    )
    user_data.sqlmodel_update(user)
    db.add(user_data)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.post("/login", response_model=Token)
async def login_for_access_token(login_data: LoginData, session: Session = Depends(get_session)) -> Token:
    user = authenticate_user(session, login_data.username, login_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

@router.post("/register", response_model=Token)
async def regisztracio(data: UserCreate, db: Session = Depends(get_session)):
    user = db.exec(select(User).where(User.username == data.username)).first()
    if user is not None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This username is unavailable",
            headers={"WWW-Authenticate": "Bearer"},
        )
    db_user = User(
        username=data.username,
    )
    db_user.password_hash = Hasher.get_password_hash(data.password)
    db.add(db_user)
    db.commit()
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")