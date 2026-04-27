from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, EmailStr, Field
from sqlalchemy.orm import Session

from config.database import get_db
from repository.user_repository import SQLUserRepository
from services.auth_service import AuthServiceImpl

router = APIRouter()


class AuthInput(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)


def get_auth_service(db: Session = Depends(get_db)) -> AuthServiceImpl:
    return AuthServiceImpl(SQLUserRepository(db))


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(input: AuthInput, service: AuthServiceImpl = Depends(get_auth_service)):
    try:
        service.register(input.email, input.password)
        return {"message": "user registered successfully"}
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.post("/login")
def login(input: AuthInput, service: AuthServiceImpl = Depends(get_auth_service)):
    try:
        token = service.login(input.email, input.password)
        return {"token": token}
    except ValueError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
