from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.db.base import Base
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


# Pydantic Models (API Schemas)
class PhotoBase(BaseModel):
    name: str = Field(..., example="vacaciones_2023.jpg")
    path: str = Field(..., example="/uploads/user1/vacaciones.jpg")
    user_id: str = Field(..., example="wbl2WeMN")
    folder_id: str = Field(..., example="AXQLDQLJ")
    date: datetime = Field(default_factory=datetime.utcnow)
    is_active: Optional[bool] = Field(None, example=False)

class PhotoCreate(PhotoBase):
    pass 


class PhotoUpdate(BaseModel):
    name: Optional[str] = Field(default=None)
    path: Optional[str] = Field(default=None)
    user_id: Optional[str] = Field(default=None)
    folder_id: Optional[str] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)

class PhotoUpdatePUT(BaseModel):
    name: str
    path: str
    user_id: str
    folder_id: str
    is_active: bool


class PhotoRead(PhotoBase):

    id: str 
    user_id: str
    folder_id: str

    model_config = {
        "from_attributes": True
    }

    