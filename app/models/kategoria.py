from sqlmodel import SQLModel, Field,Relationship
from datetime import datetime
from typing import Optional

class Kategoria(SQLModel, table=True):
    __tablename__ = "kategoriak"
    id: Optional[int] = Field(default=None, primary_key=True)
    nev: str = Field(max_length=255)
    ingatlanlink:"Ingatlan"=Relationship(back_populates="kategorianev")
 
