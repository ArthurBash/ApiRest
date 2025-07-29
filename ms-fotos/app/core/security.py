import jwt
from jwt.exceptions import InvalidTokenError
from app.core.config import settings

from fastapi import Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()

import logging
def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except InvalidTokenError:
        return None

def validate_token(credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme)):
    token = credentials.credentials
    return decode_access_token(token)

# def get_current_user(
#     token: str = Depends(oauth2_scheme),
#     db:Session = Depends(get_db)
#     ) -> User:
#     credentials_exception = HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="El token es invalido",
#         headers={"Authenticate": "Bearer"},
#     )
#     payload = decode_access_token(token)
#     if payload is None:
#         raise credentials_exception

#     user_id: str = payload.get("sub")
#     if user_id is None:
#         raise credentials_exception


#     return user