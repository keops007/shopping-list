from abc import ABC, abstractmethod
from typing import Optional

from models.user import User
from repository.user_repository import UserRepository


class ProfileService(ABC):

    @abstractmethod
    def get_profile(self, user_id: int) -> Optional[User]: ...

    @abstractmethod
    def update_avatar(self, user_id: int, avatar_url: str) -> None: ...


class ProfileServiceImpl(ProfileService):

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def get_profile(self, user_id: int) -> Optional[User]:
        return self.user_repo.find_by_id(user_id)

    def update_avatar(self, user_id: int, avatar_url: str) -> None:
        self.user_repo.update_avatar(user_id, avatar_url)
