from fastapi import APIRouter, Depends
from sqlmodel import Session
from services import book_service
from database import get_session
from models.book import Book, BookParams, BookGetParams
from typing import List
from fastapi import Query
import pdb

router = APIRouter()

@router.post("/", response_model=Book)
def add_book(
    book: Book,
    session: Session = Depends(get_session)
  ) -> Book:
    return book_service.add_book(session, book)

@router.get("/", response_model=List[Book])
def books(
    book_params: BookGetParams = Depends(),
    session: Session = Depends(get_session)
  ) -> List[Book]:
    return book_service.fetch_books(session, book_params)

@router.patch('/{id}', response_model=BookParams)
def update_book(
    id: int,
    book_params: BookParams,
    session: Session = Depends(get_session)
  ):
    return book_service.update_book(id, book_params, session)

@router.delete("/{id}", response_model=None)
def delete_book(id: int, session: Session = Depends(get_session)):
  #pdb.set_trace()
  return book_service.delete_book(id, session)
