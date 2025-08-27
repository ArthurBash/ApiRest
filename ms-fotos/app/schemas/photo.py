from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class PhotoBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la foto")
    user_id: int = Field(..., gt=0, description="ID del usuario")
    folder_id: str = Field(..., description="ID hasheado de la carpeta")


class PhotoCreate(PhotoBase):
    """Schema para crear foto"""
    pass


class PhotoUpdate(BaseModel):
    """Schema para actualizar foto"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    user_id: Optional[int] = Field(None, gt=0)
    folder_id: Optional[str] = Field(None, description="ID hasheado de la carpeta")
    is_active: Optional[bool] = None


class PhotoResponse(BaseModel):
    """Schema para respuesta de foto"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str  # ID hasheado
    name: str
    path: str
    user_id: int
    folder_id: str  # ID hasheado
    date: datetime
    is_active: bool


class PhotoUploadResponse(PhotoResponse):
    """Schema para respuesta de upload con URL"""
    upload_success: bool = True
    message: str = "Foto subida correctamente"


class PhotoPresignedUrlResponse(BaseModel):
    """Schema para URL pre-firmada"""
    photo_id: str
    url: str
    expires_in: int
    message: str = "URL generada correctamente"

