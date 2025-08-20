from sqlalchemy.orm import Session
from app.models.photo import Folder,Photo

def get_folders_by_user(user_id: str,db:Session):
    folders = (
    db.query(Folder)
    .filter(Folder.photos.any(Photo.user_id == user_id)) 
    .all()
    )
    return folders

