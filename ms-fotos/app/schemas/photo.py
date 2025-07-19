from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.base import Base
from datetime import date
from pydantic import BaseModel, Field
from typing import Optional

# SQLAlchemy Model (Database Model)
class Photo(Base):
    __tablename__ = "photos"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    path = Column(String(512), unique=True, index=True, nullable=False)
    user_id = Column(Integer, nullable=False)
    folder_id = Column(Integer, nullable=False)
    date = Column(DateTime, default=date.today(), nullable=False)
    is_active = Column(Boolean, default=True)

# Pydantic Models (API Schemas)
class PhotoBase(BaseModel):
    name: str = Field(..., example="vacaciones_2023.jpg")
    path: str = Field(..., example="/uploads/user1/vacaciones.jpg")
    user_id: int = Field(..., example=1)
    folder_id: int = Field(..., example=5)

class PhotoCreate(PhotoBase):
    pass  # Puedes añadir campos adicionales específicos para creación si es necesario

class PhotoUpdate(BaseModel):
    name: Optional[str] = Field(None, example="nuevo_nombre.jpg")
    path: Optional[str] = Field(None, example="/nueva/ruta/foto.jpg")
    user_id: Optional[int] = Field(None, example=2)
    folder_id: Optional[int] = Field(None, example=6)
    is_active: Optional[bool] = Field(None, example=False)

class PhotoRead(PhotoBase):
    id: int
    date: date
    is_active: bool

    model_config = {
        "from_attributes": True
    }
