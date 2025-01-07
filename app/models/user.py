from sqlmodel import Field, SQLModel, Relationship
from typing import Optional
from datetime import date

class UserBase(SQLModel):
    username: str = Field(default=None, max_length=64)
   
class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    password_hash: str = Field(default=None, max_length=256)
    high_score: Optional[int]
    json_save: Optional[str]
   
class UserPublicSmall(UserBase):
    id: Optional[int]
    high_score: Optional[int]
    json_save: Optional[str]

class UserPublic(UserPublicSmall):
    pass

class UserCreate(UserBase):
    password: str

class UserUpdate(UserBase):
    pass