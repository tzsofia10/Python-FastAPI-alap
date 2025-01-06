from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import date

class UserBase(SQLModel):
    name: str = Field(max_length=128)
    email: str = Field(max_length=128)
    birth_date: date
    username: Optional[str] = Field(default=None, max_length=64)
   
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: Optional[str] = Field(default=None, max_length=128)
   
class UserPublicSmall(UserBase):
    id: Optional[int]

class UserPublic(UserPublicSmall):
    pass

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass