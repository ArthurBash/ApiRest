from datetime import timedelta
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status,Path,Query
from typing import Optional


from sqlalchemy.orm import Session
from typing import List



from app.schemas.photo import PhotoCreate,PhotoRead,PhotoUpdate,PhotoUpdatePUT
from app.services.photo import (
    photo_to_id_hasheado,get_list,get_existing_photo,
    update_photo_put,update_photo_patch,delete_photo,
    PhotoService)

from app.models.photo import Photo
from app.api.deps import get_db,get_photo_service
from app.core.security import validate_token,get_current_user

from app.controller.photo_controller import handle_create_photo,get_list_photos

router = APIRouter(prefix="/api/photo", tags=["photo"])

@router.post("", response_model=PhotoRead, status_code=status.HTTP_201_CREATED)
async def api_create_photo(
    name: str = Form(...),
    user_id: str = Form(...),
    folder_id: str = Form(...),
    is_active: Optional[bool] = Form(None),
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    token_valido = Depends(validate_token)
):
   return handle_create_photo(db,name,user_id,folder_id,is_active,file)


@router.get("list_string", response_model=List[PhotoRead])
def api_list_photos(
    skip: int = 0, limit: int = 100, db: Session = Depends(get_db),
    token_valido = Depends(validate_token)):

    return get_list_photos(db,skip,limit)
    


@router.put("/{photo_id}",response_model=PhotoRead)
def api_update_photo(
    photo_id:str,
    photo_in: PhotoUpdatePUT,
    db: Session = Depends(get_db),
    photo_db: Photo = Depends(get_existing_photo),
    token_valido = Depends(validate_token)):
    
    
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
def api_delete_user(photo_db = Depends(get_existing_photo),  
    db: Session = Depends(get_db),
    token_valido = Depends(validate_token),
    photo_service: PhotoService = Depends(get_photo_service) ):

    photo_service.delete_photo_from_minio(db,photo_db.path)
    delete_photo(photo_db,db)



# @router.post("/upload")
# async def upload_image(file: UploadFile = File(...)):
#     content = await file.read()


   

@router.get("/photos")
async def get_photos(
    folder_id: Optional[str] = Query(None, description="ID hasheado de la carpeta"),
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
    user_id=Depends(get_current_user),
    photo_service: PhotoService = Depends(get_photo_service) 
):
    
    return photo_service.get_list_photos(db, user_id,  page, page_size,folder_id)
    