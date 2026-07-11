from typing import AsyncGenerator
from sqlmodel import SQLModel, create_engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True, future=True)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)

def get_sync_engine():

    return create_engine("sqlite:///./test.db", echo=True)

def create_db_and_tables():
    sync_engine = get_sync_engine()
    SQLModel.metadata.create_all(sync_engine)
