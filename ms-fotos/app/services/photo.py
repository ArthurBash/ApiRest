from sqlalchemy.orm import Session
from app.models.photo import Photo as PhotoModel
from app.schemas.photo import PhotoCreate,PhotoRead
#from app.exceptions import UsernameAlreadyExists, EmailAlreadyExists

#from passlib.context import CryptContext

from hashids import Hashids
import os
from dotenv import load_dotenv



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

