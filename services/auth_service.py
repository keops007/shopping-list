import os
from abc import ABC, abstractmethod
from datetime import datetime, timedelta, timezone

import bcrypt
from jose import jwt

from models.user import User
from repository.user_repository import UserRepository


class AuthService(ABC):

    @abstractmethod
    def register(self, email: str, password: str) -> None: ...

    @abstractmethod
    def login(self, email: str, password: str) -> str: ...


class AuthServiceImpl(AuthService):

    def __init__(self, user_repo: UserRepository):
        self.user_repo = user_repo

    def register(self, email: str, password: str) -> None:
        if self.user_repo.find_by_email(email):
            raise ValueError("user already exists")
        hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        self.user_repo.create(User(email=email, password=hashed))

    def login(self, email: str, password: str) -> str:
        user = self.user_repo.find_by_email(email)
        if not user or not bcrypt.checkpw(password.encode(), user.password.encode()):
            raise ValueError("invalid credentials")

        return jwt.encode(
            {
                "user_id": user.id,
                "email": user.email,
                "exp": datetime.now(timezone.utc) + timedelta(hours=24),
            },
            os.getenv("JWT_SECRET"),
            algorithm="HS256",
        )
