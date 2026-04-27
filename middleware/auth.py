import os
from fastapi import Header, HTTPException, status
from jose import jwt, JWTError


def get_current_user(authorization: str = Header(...)):
    token = authorization.removeprefix("Bearer ")
    try:
        payload = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="unauthorized")
