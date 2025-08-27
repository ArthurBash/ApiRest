import uuid
import os
from datetime import datetime, timedelta
from typing import Optional
import jwt
from app.schemas.user_schemas import Token, TokenData
from app.services.user_service import UserService
from app.exceptions import InvalidCredentialsError

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "clave-secreta-super-segura-cambiar-en-produccion")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """Crear token JWT"""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    def verify_token(self, token: str) -> TokenData:
        """Verificar y decodificar token JWT"""
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            user_id_str: str = payload.get("sub")
            username: str = payload.get("username")
            
            if user_id_str is None:
                raise InvalidCredentialsError()
            
            user_id = uuid.UUID(user_id_str)
            return TokenData(user_id=user_id, username=username)
        except (jwt.ExpiredSignatureError, jwt.JWTError, ValueError):
            raise InvalidCredentialsError()

    def login_user(self, username_or_email: str, password: str) -> Token:
        """Login de usuario y generación de token"""

        user = self.user_service.authenticate_user(username_or_email, password)
        
        # Crear token
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = self.create_access_token(
            data={"sub": str(user.id), "username": user.username}, 
            expires_delta=access_token_expires
        )
        
        return Token(
            access_token=access_token,
            token_type="bearer",
            expires_in=ACCESS_TOKEN_EXPIRE_MINUTES * 60  
        )

