from pydantic import BaseModel
from sqlmodel import SQLModel, Field#, Session, create_engine
from typing import Optional
from datetime import datetime
from fastapi import Query

class Book(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str
  author: str
  status: str # to_read, reading, read
  notes: Optional[str] = None
  created_at: datetime = Field(default_factory=datetime.utcnow)
  updated_at: datetime = Field(default_factory=datetime.utcnow)

  class Config:
    from_attributes = True

class BookParams(BaseModel):
  id: Optional[int] = Query(None)
  title: Optional[str] = Query(None)
  author: Optional[str] = Query(None)
  status: Optional[str] = Query(None)
  notes: Optional[str] = Query(None)