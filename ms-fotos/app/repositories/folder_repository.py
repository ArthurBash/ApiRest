from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.folder import Folder
from exceptions import FolderNotFoundError


class FolderRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, folder_data: dict) -> Folder:
        """Crear una nueva carpeta"""
        try:
            folder = Folder(**folder_data)
            self.db.add(folder)
            self.db.commit()
            self.db.refresh(folder)
            return folder
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_by_id(self, folder_id: int) -> Optional[Folder]:
        """Obtener carpeta por ID"""
        return self.db.query(Folder).filter(
            Folder.id == folder_id, 
            Folder.is_active == True
        ).first()

    def get_all(self, skip: int = 0, limit: int = 100) -> List[Folder]:
        """Obtener todas las carpetas activas"""
        return self.db.query(Folder).filter(
            Folder.is_active == True
        ).offset(skip).limit(limit).all()

    def update(self, folder_id: int, update_data: dict) -> Folder:
        """Actualizar carpeta"""
        folder = self.get_by_id(folder_id)
        if not folder:
            raise FolderNotFoundError(folder_id=str(folder_id))
        
        try:
            for key, value in update_data.items():
                if hasattr(folder, key):
                    setattr(folder, key, value)
            
            self.db.commit()
            self.db.refresh(folder)
            return folder
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def soft_delete(self, folder_id: int) -> bool:
        """Eliminado lógico de carpeta"""
        folder = self.get_by_id(folder_id)
        if not folder:
            raise FolderNotFoundError(folder_id=str(folder_id))
        
        try:
            folder.is_active = False
            self.db.commit()
            return True
        except SQLAlchemyError as e:
            self.db.rollback()
            raise e

    def get_by_path(self, path: str) -> Optional[Folder]:
        """Obtener carpeta por path"""
        return self.db.query(Folder).filter(
            Folder.path == path,
            Folder.is_active == True
        ).first()