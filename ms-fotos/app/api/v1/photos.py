from datetime import timedelta
from fastapi import APIRouter, Depends, status, Path

from sqlalchemy.orm import Session
from typing import List


from app.schemas.photo import PhotoCreate,PhotoRead,PhotoUpdate,PhotoUpdatePUT
from app.services.photo import (
    create_photo,photo_to_id_hasheado,get_list,get_existing_photo,
    update_photo_put,update_photo_patch,delete_photo)

from app.models.photo import Photo
from app.api.deps import get_db

router = APIRouter(prefix="/api/photo", tags=["photo"])


@router.post("/",response_model = PhotoRead,status_code=status.HTTP_201_CREATED)
def api_create_photo(
    photo_in : PhotoCreate, db: Session =  Depends(get_db)):
    photo = create_photo(db,photo_in)
    return photo_to_id_hasheado(photo)


@router.get("/", response_model=List[PhotoRead])
def api_list_photos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    photos = get_list(db,skip,limit)
    return [photo_to_id_hasheado(p) for p in photos]


@router.get("/{photo_id}",response_model = PhotoRead)
def api_get_photo(photo_id: str = Path(...),db: Session =  Depends(get_db)):
    photo = get_existing_photo(photo_id,db)
    return photo_to_id_hasheado(photo)



@router.put("/{photo_id}",response_model=PhotoRead)
def api_update_photo(
    photo_id:str,
    photo_in: PhotoUpdatePUT,
    db: Session = Depends(get_db),
    photo_db: Photo = Depends(get_existing_photo)):
    
    photo_update = update_photo_put(photo_db,photo_in,db)
    return photo_to_id_hasheado(photo_update)

@router.patch("/{photo_id}",response_model =PhotoRead)
def api_update_photo_patch(
    photo_in: PhotoUpdate,
    db: Session = Depends(get_db),
    photo_db: Photo = Depends(get_existing_photo)):
    
    photo_update = update_photo_patch(photo_db,photo_in,db)
    return photo_to_id_hasheado(photo_update)


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def api_delete_user(photo_db = Depends(get_existing_photo),  db: Session = Depends(get_db)):
    delete_photo(photo_db,db)

