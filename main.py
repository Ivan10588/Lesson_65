import logging
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession

from database import engine, async_session_maker, create_db_and_tables
from models import Item, ItemCreate, ItemRead

logger = logging.getLogger("uvicorn")

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app = FastAPI()

@app.get("/items/", response_model=List[ItemRead])
async def get_items(session: AsyncSession = Depends(get_session)):
    statement = select(Item)
    results = await session.exec(statement)
    items = results.all()
    logger.info("Returned %d items", len(items))
    return items

@app.get("/items/{item_id}", response_model=ItemRead)
async def get_item(item_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Item).where(Item.id == item_id)
    result = await session.exec(statement)
    item = result.one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")
    logger.debug("Item %d retrieved: %s", item.id, item.name)
    return item

@app.post("/items/", response_model=ItemRead, status_code=status.HTTP_201_CREATED)
async def create_item(item: ItemCreate, session: AsyncSession = Depends(get_session)):
    db_item = Item(**item.model_dump())
    session.add(db_item)
    await session.commit()
    await session.refresh(db_item)
    logger.info("Item created: id=%d, name=%s, price=%.2f", db_item.id, db_item.name, db_item.price)
    return db_item

@app.put("/items/{item_id}", response_model=ItemRead)
async def update_item(item_id: int, item_update: ItemCreate, session: AsyncSession = Depends(get_session)):
    statement = select(Item).where(Item.id == item_id)
    result = await session.exec(statement)
    item = result.one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    item.name = item_update.name
    item.description = item_update.description
    item.price = item_update.price
    item.tax = item_update.tax

    await session.commit()
    await session.refresh(item)
    logger.info("Item %d updated: %s", item.id, item.name)
    return item

@app.delete("/items/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_item(item_id: int, session: AsyncSession = Depends(get_session)):
    statement = select(Item).where(Item.id == item_id)
    result = await session.exec(statement)
    item = result.one_or_none()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Item not found")

    await session.delete(item)
    await session.commit()
    logger.info("Item %d deleted: %s", item.id, item.name)

@app.get("/items/search/", response_model=List[ItemRead])
async def search_items(q: str, session: AsyncSession = Depends(get_session)):
    if not q:
        return []
    statement = select(Item).where(Item.name.contains(q))
    results = await session.exec(statement)
    items = results.all()
    logger.info("Search query=%r returned %d items", q, len(items))
    return items
