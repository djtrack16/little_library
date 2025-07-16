from fastapi import HTTPException
from sqlmodel import Session, select
from models.book import Book, BookParams
from typing import List
from sqlalchemy import func
import pdb

def add_book(session: Session, book_in: Book) -> Book:
  book = Book.model_validate(book_in)
  session.add(book)
  session.commit()
  session.refresh(book)
  return book

def fetch_books(session: Session, book_params: BookParams) -> List[Book]:
  query = select(Book)
  #pdb.set_trace()
  #print("Received filters:", [id, status, author, title])
  if book_params.id:
    query = query.where(Book.id == book_params.id)

  if book_params.title:
    query = query.where(func.lower(Book.title).contains(book_params.title.lower()))
  if book_params.status:
    query = query.where(func.lower(Book.status).contains(book_params.status.lower()))
  if book_params.author:
    query = query.where(func.lower(Book.author).contains(book_params.author.lower()))

  return list(session.exec(query).all())

def delete_book(book_id: int, session: Session):
  query = select(Book).where(Book.id == book_id)
  book = session.exec(query).one
  if not book:
    raise HTTPException(status_code=404, detail="Book not found")
  session.delete(book)

def update_book(book_id: int, book_attributes: BookParams, session: Session):
  query = select(Book).where(Book.id == book_id)
  book = session.exec(query).one
  if not book:
     raise HTTPException(status_code=404, detail="Book not found")

  updated_data = book_attributes.model_dump(exclude_unset=True)
  for field, value in updated_data.items():
    setattr(book, field, value)
  
  session.commit()
  session.refresh(book)
  return book