
# schemas/user_schemas.py
import uuid
import re
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from typing import Optional


class UserBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nombre del usuario")
    lastname: str = Field(..., min_length=2, max_length=100, description="Apellido del usuario")
    username: str = Field(..., min_length=3, max_length=50, description="Nombre de usuario único")
    email: EmailStr = Field(..., description="Email del usuario")


class UserCreate(UserBase):
    """Schema para crear usuario"""
    password: str = Field(..., min_length=8, max_length=100, description="Contraseña del usuario")

    @validator('password')
    def validate_password(cls, v):
        # Al menos 2 números y 1 carácter especial
        if len(re.findall(r'\d', v)) < 2:
            raise ValueError('La contraseña debe tener al menos 2 números')
        
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('La contraseña debe tener al menos un carácter especial')
        
        return v

    @validator('username')
    def validate_username(cls, v):
        # Solo letras, números y guiones bajos
        if not re.match(r'^[a-zA-Z0-9_]+$', v):
            raise ValueError('El username solo puede contener letras, números y guiones bajos')
        return v


class UserUpdate(BaseModel):
    """Schema para actualizar usuario"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    lastname: Optional[str] = Field(None, min_length=2, max_length=100)
    username: Optional[str] = Field(None, min_length=3, max_length=50)
    email: Optional[EmailStr] = None
    password: Optional[str] = Field(None, min_length=8, max_length=100)

    @validator('password')
    def validate_password(cls, v):
        if v is not None:
            if len(re.findall(r'\d', v)) < 2:
                raise ValueError('La contraseña debe tener al menos 2 números')
            
            if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
                raise ValueError('La contraseña debe tener al menos un carácter especial')
        
        return v

    @validator('username')
    def validate_username(cls, v):
        if v is not None:
            if not re.match(r'^[a-zA-Z0-9_]+$', v):
                raise ValueError('El username solo puede contener letras, números y guiones bajos')
        return v


class UserRead(UserBase):
    """Schema para leer usuario"""
    model_config = ConfigDict(from_attributes=True)
    
    id: uuid.UUID


class UserLogin(BaseModel):
    """Schema para login"""
    username: str = Field(..., description="Username o email del usuario")
    password: str = Field(..., description="Contraseña del usuario")


class Token(BaseModel):
    """Schema para token JWT"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int = 1800  # 30 minutos en segundos


class TokenData(BaseModel):
    """Schema para datos del token"""
    user_id: uuid.UUID
    username: str