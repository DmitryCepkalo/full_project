from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from uuid import UUID, uuid4

app = FastAPI()

# ---- Модель данных ----


class Item(BaseModel):
    id: UUID
    title: str
    description: str | None = None


class ItemCreate(BaseModel):
    title: str
    description: str | None = None


# ---- "База данных" ----

items_db: Dict[UUID, Item] = {}


# ---- CREATE ----
@app.post("/items", response_model=Item)
def create_item(item: ItemCreate):
    item_id = uuid4()
    new_item = Item(
        id=item_id,
        title=item.title,
        description=item.description
    )
    items_db[item_id] = new_item
    return new_item


# ---- READ (all) ----
@app.get("/items", response_model=list[Item])
def get_items():
    return list(items_db.values())


# ---- READ (one) ----
@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: UUID):
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


# ---- UPDATE ----
@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: UUID, item_data: ItemCreate):
    item = items_db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    updated_item = Item(
        id=item_id,
        title=item_data.title,
        description=item_data.description
    )
    items_db[item_id] = updated_item
    return updated_item


# ---- DELETE ----
@app.delete("/items/{item_id}")
def delete_item(item_id: UUID):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="Item not found")

    del items_db[item_id]
    return {"status": "deleted"}
