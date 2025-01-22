from .hashing import Hasher
from typing import Annotated
from fastapi import Cookie, HTTPException, Depends, status, Header
from sqlmodel import Session, select
from ..models.user import User
import os
from dotenv import load_dotenv
from datetime import datetime, timezone, timedelta
from pydantic import BaseModel
import jwt
from jwt.exceptions import InvalidTokenError
from ..database import get_session
import logging

logger = logging.getLogger("uvicorn.error")
logger.setLevel(logging.DEBUG)

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

if SECRET_KEY is None:
    raise Exception("Set SECRET_KEY in .env")
if ALGORITHM is None:
    raise Exception("Set ALGORITHM in .env")
if ACCESS_TOKEN_EXPIRE_MINUTES is None:
    raise Exception("Set ACCESS_TOKEN_EXPIRE_MINUTES in .env")

class Token(BaseModel):
    access_token: str
    token_type: str

class LoginData(BaseModel):
    username: str
    password: str

def authenticate_user(session: Session, username: str, password: str) -> User:
    query = select(User).where(User.username == username)
    user = session.exec(query).unique().first()
    if not user:
        return False
    if not Hasher.verify_password(password, user.password_hash):
        return False
    return user



def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(authorization: Annotated[str | None, Header()] = None, authtoken: Annotated[str | None, Cookie()] = None, session: Session = Depends(get_session)) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = ""
    if authorization:
        authtoken = authorization.split(' ')[1]
    try:
        payload = jwt.decode(authtoken, SECRET_KEY, algorithms=[ALGORITHM])
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except InvalidTokenError as e:
        raise credentials_exception
    query = select(User).where(User.username == username)
    user = session.exec(query).unique().first()
    if user is None:
       raise credentials_exception
    return user