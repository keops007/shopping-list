from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from models.shopping_item import ShoppingItem


class ShoppingRepository(ABC):

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> List[ShoppingItem]: ...

    @abstractmethod
    def find_by_id_and_user_id(self, id: int, user_id: int) -> Optional[ShoppingItem]: ...

    @abstractmethod
    def create(self, item: ShoppingItem) -> ShoppingItem: ...

    @abstractmethod
    def set_done(self, id: int, done: bool) -> None: ...

    @abstractmethod
    def delete(self, id: int, user_id: int) -> int: ...


class SQLShoppingRepository(ShoppingRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_by_user_id(self, user_id: int) -> List[ShoppingItem]:
        return (
            self.db.query(ShoppingItem)
            .filter(ShoppingItem.user_id == user_id)
            .order_by(ShoppingItem.done.asc(), ShoppingItem.created_at.desc())
            .all()
        )

    def find_by_id_and_user_id(self, id: int, user_id: int) -> Optional[ShoppingItem]:
        return (
            self.db.query(ShoppingItem)
            .filter(ShoppingItem.id == id, ShoppingItem.user_id == user_id)
            .first()
        )

    def create(self, item: ShoppingItem) -> ShoppingItem:
        self.db.add(item)
        self.db.commit()
        self.db.refresh(item)
        return item

    def set_done(self, id: int, done: bool) -> None:
        self.db.query(ShoppingItem).filter(ShoppingItem.id == id).update({"done": done})
        self.db.commit()

    def delete(self, id: int, user_id: int) -> int:
        count = (
            self.db.query(ShoppingItem)
            .filter(ShoppingItem.id == id, ShoppingItem.user_id == user_id)
            .delete()
        )
        self.db.commit()
        return count
