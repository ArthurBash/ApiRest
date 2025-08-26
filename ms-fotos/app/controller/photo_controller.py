from sqlalchemy.orm import Session
from app.services.photo import create_photo_entry
from fastapi import UploadFile
from app.services.photo import  photo_to_id_hasheado,get_list

async def handle_create_photo(
    db: Session,
    name: str,
    user_id: str,
    folder_id: str,
    is_active: bool,
    file: UploadFile
):
  
    photo = create_photo_entry(db,name,user_id,folder_id,is_active,file)
    return photo_to_id_hasheado(photo)


async def get_list_photos(
    db:Session,
    skip:int,
    limit:int
):
    photos = get_list(db,skip,limit)
    return [photo_to_id_hasheado(p) for p in photos]