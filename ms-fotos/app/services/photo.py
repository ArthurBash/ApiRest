from sqlalchemy.orm import Session
from app.models.photo import Photo as PhotoModel
from app.schemas.photo import PhotoCreate,PhotoRead
#from app.exceptions import UsernameAlreadyExists, EmailAlreadyExists

#from passlib.context import CryptContext

# app/services/hashid_service.py
#from hashids import Hashids
#import os
#from dotenv import load_dotenv



def create_photo(db: Session, photo_in: PhotoCreate):
    db_photo = PhotoModel(
        name = photo_in.name,
        user_id = photo_in.user_id,
        folder_id = photo_in.folder_id,
        date = photo_in.date,
        is_active = photo_in.is_active

    )
