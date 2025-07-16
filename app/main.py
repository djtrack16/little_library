from typing import Union

from fastapi import FastAPI, APIRouter
from sqlmodel import SQLModel, create_engine, Session
from models.book import Book
from routes import router as book_router

app = FastAPI()
engine = create_engine('sqlite:///./littlelibrary.db', echo=True)

@app.on_event("startup")
def on_startup():
  SQLModel.metadata.create_all(engine)

app.include_router(book_router, prefix="/books", tags=["books"])