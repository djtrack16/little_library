import sys
import os
import pytest
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, create_engine, Session, select
from factories.book_factory import BookFactory as BaseBookFactory
from factories.book_factory import BookParamsFactory
from sqlalchemy.pool import StaticPool
from sqlalchemy import text
from main import app
from database import get_session
from models.book import Book, BookParams
import pdb

# Fix Python path for module imports
# this is here so app can be a valid dir to load.... TODO CHANGE LATER
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))



TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
  TEST_DATABASE_URL,
  connect_args={"check_same_thread": False},
  poolclass=StaticPool
)

test_session = Session(engine)

# Create schema once globally when test session starts
SQLModel.metadata.create_all(engine)

# Shared session for override
def override_get_session():
  yield test_session

app.dependency_overrides[get_session] = override_get_session
client = TestClient(app)

@pytest.fixture(scope="session")
def db_engine():
  yield engine
  #SQLModel.metadata.drop_all(engine)

@pytest.fixture(scope="function")
def db_session():
  yield test_session
  #SQLModel.metadata.drop_all(engine)

  # Teardown: Clear the Book table after each test
  test_session.exec(text('DELETE FROM book')) # type: ignore
  test_session.commit()

@pytest.fixture
def book_factory(db_session):
  # Bind the test session to the factory
  BaseBookFactory._meta.sqlalchemy_session = db_session  # type: ignore[attr-defined]
  return BaseBookFactory

def make_book_factory_with_session(session):
  class BookFactoryWithSession(BaseBookFactory):
    class Meta:
      model = BaseBookFactory._meta.model
      sqlalchemy_session = session
      sqlalchemy_session_persistence = "flush"
  return BookFactoryWithSession

def make_book_param_factory_with_session(session):
  class BookParamFactoryWithSession(BookParamsFactory):
    class Meta:
      model = BaseBookFactory._meta.model
      sqlalchemy_session = session
      sqlalchemy_session_persistence = "flush"
  return BookParamFactoryWithSession

@pytest.fixture
def book_factory_with_session(db_session):
  return lambda **kwargs: BaseBookFactory(sqlalchemy_session=db_session, **kwargs)

def test_add_book(db_session):
  BookFactory = make_book_factory_with_session(db_session)
  book = BookFactory()
  payload = book.model_dump(exclude_unset=True, exclude={"id"})
  response = client.post("/books", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["title"] == book.title
  assert data["author"] == book.author
  assert data["status"] == book.status
  assert data["notes"] == book.notes

def test_delete_book(db_session):
  BookFactory = make_book_factory_with_session(db_session)
  book = BookFactory()
  db_session.commit()
  response = client.delete(f"/books/{book.id}")
  assert response.status_code == 204
  deleted_book = db_session.get(Book, book.id)
  assert deleted_book is None

def test_update_book(db_session):
  BookParamsFactory = make_book_param_factory_with_session(db_session)
  book_params = BookParamsFactory()
  payload = book_params.model_dump(exclude_unset=True, exclude={"id"})
  db_session.commit()
  payload = {"author": "author", "title": "title"}
  response = client.patch(f"/books/{book_params.id}", json=payload)
  assert response.status_code == 200
  data = response.json()
  assert data["title"] == "title"
  assert data["author"] == "author"

def test_get_books_by_author(book_factory):
  book = book_factory(author="Ursula K. Le Guin")
  response = client.get("/books/?author=ursula")

  assert response.status_code == 200
  data = response.json()
  assert len(data) == 1
  assert "ursula" in data[0]["author"].lower()

def test_get_books_by_id(book_factory):
  book = book_factory(author="blah blah")
  response = client.get(f"/books/?id={book.id}")
  assert response.status_code == 200
  data = response.json()
  assert len(data) == 1
  assert data[0]["id"] == book.id

def test_get_books_by_title(book_factory):
  book = book_factory(title="All Science Fiction")
  response = client.get("/books/?title=science")
  assert response.status_code == 200
  data = response.json()
  assert len(data) == 1
  assert "science" in data[0]["title"].lower()

def test_get_books_by_status(book_factory):
  status = "reading"
  book = book_factory(status=status)
  response = client.get(f"/books/?status={status}")
  assert response.status_code == 200
  data = response.json()
  assert len(data) == 1
  assert data[0]["status"].lower() == status
