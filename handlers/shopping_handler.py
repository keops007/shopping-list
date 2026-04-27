from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session

from config.database import get_db
from middleware.auth import get_current_user
from repository.shopping_repository import SQLShoppingRepository
from services.shopping_service import ShoppingServiceImpl

router = APIRouter()


class ItemInput(BaseModel):
    name: str


def get_shopping_service(db: Session = Depends(get_db)) -> ShoppingServiceImpl:
    return ShoppingServiceImpl(SQLShoppingRepository(db))


def serialize(item):
    return {
        "id": item.id,
        "user_id": item.user_id,
        "name": item.name,
        "done": item.done,
        "created_at": item.created_at,
    }


@router.get("/shopping")
def get_items(
    current_user: dict = Depends(get_current_user),
    service: ShoppingServiceImpl = Depends(get_shopping_service),
):
    return [serialize(i) for i in service.get_items(current_user["user_id"])]


@router.post("/shopping", status_code=status.HTTP_201_CREATED)
def add_item(
    input: ItemInput,
    current_user: dict = Depends(get_current_user),
    service: ShoppingServiceImpl = Depends(get_shopping_service),
):
    return serialize(service.add_item(current_user["user_id"], input.name))


@router.patch("/shopping/{id}/done")
def toggle_item(
    id: int,
    current_user: dict = Depends(get_current_user),
    service: ShoppingServiceImpl = Depends(get_shopping_service),
):
    try:
        return serialize(service.toggle_item(id, current_user["user_id"]))
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item negasit")


@router.delete("/shopping/{id}")
def delete_item(
    id: int,
    current_user: dict = Depends(get_current_user),
    service: ShoppingServiceImpl = Depends(get_shopping_service),
):
    try:
        service.delete_item(id, current_user["user_id"])
        return {"message": "sters"}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="item negasit")
