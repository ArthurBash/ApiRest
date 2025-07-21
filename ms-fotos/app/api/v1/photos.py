from datetime import timedelta
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List


from app.schemas.photo import PhotoCreate,PhotoRead
from app.services.photo import create_photo,photo_to_id_hasheado
#from fastapi.security import OAuth2PasswordRequestForm
#from app.schemas.auth import Token
from app.api.deps import get_db
from app.models.photo import Photo


router = APIRouter(prefix="/api/photo", tags=["photo"])


@router.post("/",response_model = PhotoRead,status_code=status.HTTP_201_CREATED)
def api_create_photo(
    photo_in : PhotoCreate, db: Session =  Depends(get_db)):

    photo = create_photo(db,photo_in)
    return photo_to_id_hasheado(photo)


@router.get("/", response_model=List[PhotoRead])
def api_list_photos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    photos = db.query(Photo).offset(skip).limit(limit).all()
    return [photo_to_id_hasheado(p) for p in photos]