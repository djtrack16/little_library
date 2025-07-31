
from fastapi import FastAPI#, APIRouter
from sqlmodel import SQLModel, create_engine#, Session
from routes import router as book_router
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
  # Startup: create DB tables
  SQLModel.metadata.create_all(engine)
  yield
  # Shutdown: nothing needed here, but could close resources if required

app = FastAPI(lifespan=lifespan)
engine = create_engine('sqlite:///./littlelibrary.db', echo=True)

app.include_router(book_router, prefix="/books", tags=["books"])