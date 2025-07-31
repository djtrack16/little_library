from pydantic import BaseModel, ConfigDict
from sqlmodel import SQLModel, Field#, Session, create_engine
from typing import Optional
from datetime import datetime, UTC
from fastapi import Query

class Book(SQLModel, table=True):
  id: Optional[int] = Field(default=None, primary_key=True)
  title: str
  author: str
  status: str # to_read, reading, read
  notes: Optional[str] = None
  created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
  updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))

  #class Config:
  #  from_attributes = True
#
class BookParams(BaseModel):
  id: Optional[int] = None
  title: Optional[str] = None
  author: Optional[str] = None
  status: Optional[str] = None
  notes: Optional[str] = None

  model_config = ConfigDict(from_attributes=True)

class BookGetParams(BaseModel):
  id: Optional[int] = None
  title: Optional[str] = None
  author: Optional[str] = None
  status: Optional[str] = None
  notes: Optional[str] = None

  model_config = ConfigDict(from_attributes=True)
