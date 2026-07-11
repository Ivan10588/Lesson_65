from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = 0.0

from fastapi import FastAPI, HTTPException
from typing import List

app = FastAPI()

items_db: List[Item] = []

@app.get("/items/", response_model=List[Item])
def get_items():
    return items_db

@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    for item in items_db:
        if item.id == item_id:
            return item
    raise HTTPException(status_code=404, detail="Item not found")

@app.post("/items/")
def create_item(item: Item):
    items_db.append(item)
    return {"message": f"Item {item.name} added", "item": item}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    for i, stored_item in enumerate(items_db):
        if stored_item.id == item_id:
            items_db[i] = item
            return {"message": "Item updated", "item": item}
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    for i, item in enumerate(items_db):
        if item.id == item_id:
            deleted_item = items_db.pop(i)
            return {"message": "Item deleted", "item": deleted_item}
    raise HTTPException(status_code=404, detail="Item not found")
