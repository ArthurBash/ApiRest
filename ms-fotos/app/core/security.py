import jwt
from jwt.exceptions import InvalidTokenError
from app.core.config import settings

from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status

from app.services.photo import decode_id
from fastapi.security import OAuth2PasswordBearer

import logging

bearer_scheme = HTTPBearer()
# Esquema de autenticación
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/users/token/login")


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except InvalidTokenError:
        return None

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    return decode_access_token(token)


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)) -> str:
    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token es inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user_id: str = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="El token es inválido",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return decode_id(user_id)