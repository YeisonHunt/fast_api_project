from pydantic import BaseModel
from typing import List, Optional

# Item schemas
class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    name: str
    email: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    items: List[Item] = []

    class Config:
        from_attributes = True