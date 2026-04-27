from abc import ABC, abstractmethod
from typing import List

from models.shopping_item import ShoppingItem
from repository.shopping_repository import ShoppingRepository


class ShoppingService(ABC):

    @abstractmethod
    def get_items(self, user_id: int) -> List[ShoppingItem]: ...

    @abstractmethod
    def add_item(self, user_id: int, name: str) -> ShoppingItem: ...

    @abstractmethod
    def toggle_item(self, id: int, user_id: int) -> ShoppingItem: ...

    @abstractmethod
    def delete_item(self, id: int, user_id: int) -> None: ...


class ShoppingServiceImpl(ShoppingService):

    def __init__(self, repo: ShoppingRepository):
        self.repo = repo

    def get_items(self, user_id: int) -> List[ShoppingItem]:
        return self.repo.find_by_user_id(user_id)

    def add_item(self, user_id: int, name: str) -> ShoppingItem:
        return self.repo.create(ShoppingItem(user_id=user_id, name=name))

    def toggle_item(self, id: int, user_id: int) -> ShoppingItem:
        item = self.repo.find_by_id_and_user_id(id, user_id)
        if not item:
            raise ValueError("item not found")
        item.done = not item.done
        self.repo.set_done(id, item.done)
        return item

    def delete_item(self, id: int, user_id: int) -> None:
        if self.repo.delete(id, user_id) == 0:
            raise ValueError("item not found")
