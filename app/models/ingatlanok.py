from sqlmodel import SQLModel, Field, Relationship
from datetime import date, datetime
from typing import Optional
from .kategoria import Kategoria

class IngatlanBase(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    leiras: str = Field(max_length=255)
    hirdetesDatum:date=Field(default_factory=datetime.utcnow)
    kategoria:int=Field(foreign_key="kategoriak.id")
    tehermentes:bool=Field()
    ar:int=Field()
    kepURL:str=Field(max_length=255)
class Ingatlan(IngatlanBase, table=True):
    __tablename__ = "ingatlanok"
    kategorianev:Kategoria=Relationship(back_populates="ingatlanlink")
    
 
class IngatlanPublic(IngatlanBase):
    kategorianev:Kategoria