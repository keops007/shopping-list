import os
import pathlib
import shutil

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session

from config.database import get_db
from middleware.auth import get_current_user
from repository.user_repository import SQLUserRepository
from services.profile_service import ProfileServiceImpl

router = APIRouter()

ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".webp"}


def get_profile_service(db: Session = Depends(get_db)) -> ProfileServiceImpl:
    return ProfileServiceImpl(SQLUserRepository(db))


@router.get("/profile")
def get_profile(
    current_user: dict = Depends(get_current_user),
    service: ProfileServiceImpl = Depends(get_profile_service),
):
    user = service.get_profile(current_user["user_id"])
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="user not found")
    return {"id": user.id, "email": user.email, "avatar": user.avatar or ""}


@router.post("/profile/avatar")
def upload_avatar(
    file: UploadFile = File(...),
    current_user: dict = Depends(get_current_user),
    service: ProfileServiceImpl = Depends(get_profile_service),
):
    ext = pathlib.Path(file.filename).suffix.lower()
    if ext not in ALLOWED_EXTS:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="format neacceptat (jpg, png, webp)")

    os.makedirs("./uploads", exist_ok=True)
    filename = f"{current_user['user_id']}{ext}"
    save_path = f"./uploads/{filename}"

    with open(save_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    avatar_url = f"/uploads/{filename}"
    service.update_avatar(current_user["user_id"], avatar_url)
    return {"avatar": avatar_url}
