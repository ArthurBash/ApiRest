from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional

class FolderBase(BaseModel):
    name: str = Field(..., example="Vacaciones 2023")
    path: str = Field(..., example="/folders/vacaciones_2023")
    is_active: Optional[bool] = Field(True, example=True)

class FolderCreate(FolderBase):
    pass 


class FolderRead(FolderBase):
    id: str = Field(..., example="AXQLDQLJ")
    date_created: datetime = Field(..., example="2023-12-01T10:30:00")

    model_config = {
        "from_attributes": True
    }

class FolderResponse(BaseModel):
    id: str
    name: str
    path: str
    date_created: datetime
    is_active: bool
    photos_count: Optional[int] = Field(default=0, description="Número de fotos en la carpeta")

    model_config = {
        "from_attributes": True
    }

class FolderListResponse(BaseModel):
    folders: List[FolderResponse]
    total: int
    page: int
    page_size: int
    has_next: bool