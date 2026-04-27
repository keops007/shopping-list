from abc import ABC, abstractmethod
from typing import Optional
from sqlalchemy.orm import Session
from models.user import User


# ABC = Abstract Base Class — echivalentul interfetei din Go
class UserRepository(ABC):

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]: ...

    @abstractmethod
    def find_by_id(self, id: int) -> Optional[User]: ...

    @abstractmethod
    def create(self, user: User) -> User: ...

    @abstractmethod
    def update_avatar(self, id: int, avatar_url: str) -> None: ...


# SQLUserRepository este implementarea concreta — foloseste SQLAlchemy + PostgreSQL
class SQLUserRepository(UserRepository):

    def __init__(self, db: Session):
        self.db = db

    def find_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()

    def find_by_id(self, id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == id).first()

    def create(self, user: User) -> User:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)
        return user

    def update_avatar(self, id: int, avatar_url: str) -> None:
        self.db.query(User).filter(User.id == id).update({"avatar": avatar_url})
        self.db.commit()
