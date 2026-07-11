from typing import Optional
from pydantic import Field
from sqlmodel import SQLModel, Field

class Item(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = Field(default=0.0)

class ItemCreate(SQLModel):
    name: str = Field(..., min_length=1)
    description: Optional[str] = None
    price: float = Field(..., gt=0, description="Price must be greater than 0")
    tax: Optional[float] = Field(default=0.0, ge=0)

class ItemRead(Item):

    pass
