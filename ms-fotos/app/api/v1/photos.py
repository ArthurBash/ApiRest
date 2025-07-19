from datetime import timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List


from app.schemas.photo import PhotoCreate,PhotoRead
from app.services.photo import create_photo
#from fastapi.security import OAuth2PasswordRequestForm
#from app.schemas.auth import Token
from app.api.deps import get_db

router = APIRouter(prefix="/api/photo", tags=["photo"])


@router.post("/",response_model = PhotoRead,status_code=status.HTTP_201_CREATED)
def api_create_photo(
    photo_in : PhotoCreate, db: Session =  Depends(get_db)):

    photo = create_photo(db,user_in)
    return photo
