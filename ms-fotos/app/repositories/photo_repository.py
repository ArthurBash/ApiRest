

from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import List, Optional, Tuple
from app.models.photo import Photo


from app.exceptions import PhotoNotFoundError, PhotoUpdateError, DatabaseError

class PhotoRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_photos_by_folder(
        self, 
        user_id: int, 
        folder_id: int, 
        page: int = 1, 
        page_size: int = 20
    ) -> tuple[List[Photo], int]:
        """Obtiene fotos por folder_id con paginación"""
        query = self.db.query(Photo).filter(
            and_(
                Photo.user_id == user_id,
                Photo.folder_id == folder_id,
                Photo.is_active == True
            )
        ).order_by(Photo.date.desc())
        
        total = query.count()
        offset = (page - 1) * page_size
        photos = query.offset(offset).limit(page_size).all()
        
        return photos, total

    def get_photos_by_user(
        self, 
        user_id: int, 
        page: int = 1, 
        page_size: int = 20
    ) -> tuple[List[Photo], int]:
        """Obtiene todas las fotos de un usuario con paginación"""
        query = self.db.query(Photo).filter(
            and_(
                Photo.user_id == user_id,
                Photo.is_active == True
            )
        ).order_by(Photo.date.desc())
        
        total = query.count()
        offset = (page - 1) * page_size
        photos = query.offset(offset).limit(page_size).all()
        
        return photos, total

    def get_photo_user_by_id(self, photo_id: int, user_id: int) -> Optional[Photo]:
        """Obtiene una foto específica por ID (verificando ownership)"""
        return self.db.query(Photo).filter(
            and_(
                Photo.id == photo_id,
                Photo.user_id == user_id,
                Photo.is_active == True
            )
        ).first()


    
    
    