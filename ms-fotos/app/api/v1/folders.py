from fastapi import APIRouter,    Depends, HTTPException, status,Path,Query
from app.core.security import validate_token
from app.api.deps import get_db

from sqlalchemy.orm import Session
from typing import List
from app.schemas.folder import FolderRead,FolderCreate


from app.services.folder import get_folders_list,folder_to_id_hasheado,create_folder_entry

router = APIRouter(prefix="/api/photo", tags=["Folder"])

@router.get("/folders", response_model=List[FolderRead])
def api_list_folders(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    token_valido = Depends(validate_token)
):
    folders = get_folders_list(db, skip, limit)
    return [folder_to_id_hasheado(f) for f in folders]


@router.post("/folders", response_model=FolderRead, status_code=201)
def api_create_folder(
    folder_data: FolderCreate,
    db: Session = Depends(get_db),
    token_valido = Depends(validate_token)
):
    folder = create_folder_entry(db, folder_data)
    return folder_to_id_hasheado(folder)

