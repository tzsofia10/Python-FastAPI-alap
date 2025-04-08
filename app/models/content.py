from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Content(SQLModel, table=True):
    __tablename__ = "contents"
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(max_length=255)
    body: str
    img: Optional[str] = Field(default=None, max_length=255)
    created_at: datetime = Field(default_factory=datetime.utcnow)
