import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from factory.faker import Faker
from factory.alchemy import SQLAlchemyModelFactory
from models.book import Book, BookParams, BookGetParams
from factory.declarations import Sequence, Iterator

class BookFactory(SQLAlchemyModelFactory):
  class Meta:
    model = Book
    sqlalchemy_session = None  # This gets set in tests
    sqlalchemy_session_persistence = "flush"  # or "commit"

  title = Faker("sentence", nb_words=3)
  author = Faker("name")
  status = "reading"
  notes = Faker("text", max_nb_chars=50)



class BookParamsFactory(SQLAlchemyModelFactory):
  class Meta:
    model = BookParams
    sqlalchemy_session = None  # This gets set in tests
    sqlalchemy_session_persistence = "flush"  # or "commit"

  title = Faker("sentence", nb_words=3)
  author = Faker("name")
  status = "reading"
  notes = Faker("text", max_nb_chars=50)

'''
class BookGetParamsFactory(SQLAlchemyModelFactory):
  class Meta:
    model = BookGetParams

  id = Faker("random_int", min=1, max=100)
  title = Faker("sentence", nb_words=3)
  author = Faker("name")
  status = factory.Iterator(["reading", "completed", "wishlist"])
  notes = Faker("sentence")
'''