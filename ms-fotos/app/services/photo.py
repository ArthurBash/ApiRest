from sqlalchemy.orm import Session
from app.models.photo import Photo as PhotoModel
from app.schemas.photo import PhotoCreate,PhotoRead
from app.models.photo import Photo
from fastapi import  Depends,Path
from app.api.deps import get_db
from app.schemas.photo import PhotoUpdate, PhotoUpdatePUT



from app.exceptions import ErrorDecodificacion,ErrorFotoNoEncontrada
#from passlib.context import CryptContext

from hashids import Hashids
import os
from dotenv import load_dotenv

def get_list(db,skip,limit):
    return db.query(Photo).offset(skip).limit(limit).all()


def get_existing_photo(photo_id: str = Path(...), db: Session = Depends(get_db)):
    try:
        decoded_id = decode_id(photo_id)
    except Exception:
        raise ErrorDecodificacion()

    photo = db.query(Photo).filter_by(id=decoded_id).first()

    if not photo:
        raise ErrorFotoNoEncontrada()
    return photo


def create_photo(db: Session, photo_in: PhotoCreate):
    user_id_int = decode_id(photo_in.user_id)      
    folder_id_int = decode_id(photo_in.folder_id)  

    db_photo = PhotoModel(
        name = photo_in.name,
        user_id = user_id_int,
        folder_id = folder_id_int,
        date = photo_in.date,
        path = photo_in.path,
        is_active = photo_in.is_active

    )
    db.add(db_photo)
    db.commit()
    db.refresh(db_photo)
    return db_photo


def update_photo_patch(photo_db:Photo, photo_in: PhotoUpdate, db: Session):
    

    photo_data = photo_in.dict(exclude_unset=True)  
    for field, value in photo_data.items():
        setattr(photo_db, field, value)

    db.add(photo_db)
    db.commit()
    db.refresh(photo_db)
    return photo_db

def update_photo_put(photo_db: Photo, photo_in: PhotoUpdatePUT, db: Session):
    
    photo_db.name = photo_in.name
    photo_db.path = photo_in.path
    photo_db.user_id = photo_in.user_id
    photo_db.folder_id = photo_in.folder_id
    photo_db.is_active = photo_in.is_active

    db.add(photo_db)
    db.commit()
    db.refresh(photo_db)
    return photo_db

def delete_photo(photo_db):
    db.delete(photo_db)
    db.commit()

load_dotenv() 

HASHIDS_SALT = os.getenv("HASHIDS_SALT", "valor_por_defecto_no_conveniente")
HASHIDS_MIN_LENGTH = int(os.getenv("HASHIDS_MIN_LENGTH", 8))

hashids = Hashids(salt=HASHIDS_SALT, min_length=HASHIDS_MIN_LENGTH)

def encode_id(id: int) -> str:
    return hashids.encode(id)

def decode_id(hashid: str) -> int:
    decoded = hashids.decode(hashid)
    if decoded:
        return decoded[0]
    raise ValueError("ID inválido")

def photo_to_id_hasheado(photo) -> PhotoRead:
    return PhotoRead(
        id = encode_id(photo.id),   
        name = photo.name,
        path = photo.path,
        user_id = encode_id(photo.user_id),
        folder_id= encode_id(photo.folder_id),
        is_active = photo.is_active,
        date = photo.date
    )




