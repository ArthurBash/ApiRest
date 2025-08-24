from sqlalchemy.orm import Session
from app.models.photo import Photo
from app.models.folder import Folder
from app.schemas.folder import FolderRead,FolderCreate

from app.utils import encode_id,decode_id

def get_folders_by_user(user_id: str,db:Session):
    folders = (
    db.query(Folder)
    .filter(Folder.photos.any(Photo.user_id == user_id)) 
    .all()
    )
    return folders

def get_folders_list(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Folder).filter(
        Folder.is_active == True
    ).offset(skip).limit(limit).all()


def folder_to_id_hasheado(folder) -> FolderRead:
    return FolderRead(
        id = encode_id(folder.id),
        name = folder.name,
        path = folder.path,
        is_active = folder.is_active,
        date_created = folder.date_created
    )

def create_folder_entry(db: Session, folder_data: FolderCreate):
    # Verificar si ya existe una carpeta con el mismo path
    existing_folder = db.query(Folder).filter(
        Folder.path == folder_data.path,
        Folder.is_active == True
    ).first()
    
    if existing_folder:
        raise HTTPException(
            status_code=400,
            detail=f"Folder with path '{folder_data.path}' already exists"
        )
    
    folder = Folder(
        name=folder_data.name,
        path=folder_data.path,
        is_active=folder_data.is_active if folder_data.is_active is not None else True
    )
    
    db.add(folder)
    db.commit()
    db.refresh(folder)
    
    return folder
