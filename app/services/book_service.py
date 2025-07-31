from fastapi import HTTPException, Response
from sqlmodel import Session, select
from models.book import Book, BookParams, BookGetParams
from typing import List
from sqlalchemy import func
import pdb
from sqlalchemy.exc import IntegrityError, NoResultFound

def add_book(session: Session, book_in: Book) -> Book:
  book = Book.model_validate(book_in)
  session.add(book)
  session.commit()
  session.refresh(book)
  return book

def fetch_books(session: Session, book_params: BookGetParams) -> List[Book]:
  query = select(Book)
  #pdb.set_trace()
  #print("Received filters:", [id, status, author, title])
  if book_params.id:
    query = query.where(Book.id == book_params.id)

  if book_params.title:
    query = query.where(func.lower(Book.title).contains(book_params.title.lower()))
  if book_params.status:
    print(book_params)
    query = query.where(Book.status.ilike(f"%{book_params.status}%")) # type: ignore

    #query = query.where(func.lower(Book.status) == book_params.status.lower())
  if book_params.author:
    query = query.where(func.lower(Book.author).contains(book_params.author.lower()))
  books = list(session.exec(query).all())
  print([b.status for b in books])
  return books

def delete_book(book_id: int, session: Session):
  try:
    query = select(Book).where(Book.id == book_id)
    book = session.exec(query).one_or_none()
    if not book:
      raise_404(f"Book with id={book_id} not found")
    session.delete(book)
    session.commit()
    return Response(status_code=204)
    session.rollback()
    print(f"Integrity Error: {e}")
  except Exception as e:
    session.rollback()
    print(f"An unexpected error occurred: {e}")

def update_book(book_id: int, book_attributes: BookParams, session: Session):
  query = select(Book).where(Book.id == book_id)
  book = session.exec(query).one_or_none()
  if not book:
     raise_404(f"Book with id={book_id} not found")

  updated_data = book_attributes.model_dump(exclude_unset=True)
  for field, value in updated_data.items():
    setattr(book, field, value)
  
  session.commit()
  session.refresh(book)
  return book

def raise_404(str):
  raise HTTPException(status_code=404, detail=str)

