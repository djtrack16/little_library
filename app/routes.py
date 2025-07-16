from fastapi import APIRouter, Depends
from sqlmodel import Session
from services import book_service
from database import get_session
from models.book import Book, BookParams
from typing import List
from fastapi import Query

router = APIRouter()

@router.post("/", response_model=Book)
def add_book(
    book: Book,
    session: Session = Depends(get_session)
  ) -> Book:
    return book_service.add_book(session, book)

@router.get("/", response_model=List[Book])
def books(
    session: Session = Depends(get_session),
    book_params: BookParams = Depends()
  ) -> List[Book]:
    return book_service.fetch_books(session, book_params)

@router.patch('/{book_id}', response_model=Book)
def update_book(
    book_id: int,
    session: Session = Depends(get_session),
    book_params: BookParams = Depends()
  ):
    return book_service.update_book(book_id, book_params, session)

@router.delete("/", response_model=None)
def delete_book(book_id: int, session: Session = Depends(get_session)):
  return book_service.delete_book(book_id, session)
