from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.models import Item, User
from app.schemas.schemas import Item as ItemSchema, ItemCreate

router = APIRouter()


@router.get("/items/{item_id}", response_model=ItemSchema)
def get_item(item_id: int, db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.post("/users/{user_id}/items/", response_model=ItemSchema)
def create_item_for_user(user_id: int, item: ItemCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    db_item = Item(**item.dict(), owner_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item