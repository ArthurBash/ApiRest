from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class FolderBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255, description="Nombre de la carpeta")
    path: str = Field(..., min_length=1, max_length=512, description="Ruta de la carpeta")


class FolderCreate(FolderBase):
    """Schema para crear carpeta"""
    pass


class FolderUpdate(BaseModel):
    """Schema para actualizar carpeta"""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    path: Optional[str] = Field(None, min_length=1, max_length=512)
    is_active: Optional[bool] = None


class FolderResponse(FolderBase):
    """Schema para respuesta de carpeta"""
    model_config = ConfigDict(from_attributes=True)
    
    id: str  # ID hasheado
    date_created: datetime
    is_active: bool