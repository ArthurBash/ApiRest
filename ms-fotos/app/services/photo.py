from sqlalchemy.orm import Session
from app.models.photo import Photo as PhotoModel
from app.schemas.photo import PhotoCreate,PhotoRead
from app.models.photo import Photo
from fastapi import  Depends,Path,HTTPException,UploadFile

from app.api.deps import get_db
from app.schemas.photo import PhotoUpdate, PhotoUpdatePUT

from minio import Minio


from app.exceptions import DecodingError,PhotoNotFoundError,FileNotValidate,FolderNotFoundError
#from passlib.context import CryptContext

from app.utils import encode_id,decode_id
from fastapi.responses import StreamingResponse
import os
from app.models.folder import Folder

#s3

# import boto3
# from botocore.client import Config

#minio
from fastapi import  File, UploadFile, HTTPException
from uuid import uuid4
from app.services.minio_client import get_minio_client

def get_list(db,skip,limit):
    return db.query(Photo).offset(skip).limit(limit).all()


def get_existing_photo(photo_id: str = Path(...), db: Session = Depends(get_db)):
    decoded_id = decode_id(photo_id)
    
    photo = db.query(Photo).filter_by(id=decoded_id).first()

    if not photo:
        raise PhotoNotFoundError()
    return photo




def update_photo_patch(photo_db:Photo, photo_in: PhotoUpdate, db: Session):
    

    photo_data = photo_in.dict(exclude_unset=True)

    if "folder_id" in photo_data:
        photo_data["folder_id"] = decode_id(photo_data["folder_id"])

    if "user_id" in photo_data:
        photo_data["user_id"] = decode_id(photo_data["user_id"])

    # Asignar los campos al modelo
    for field, value in photo_data.items():
        setattr(photo_db, field, value)

    db.add(photo_db)
    db.commit()
    db.refresh(photo_db)
    return photo_db

def update_photo_put(photo_db: Photo, photo_in: PhotoUpdatePUT, db: Session):
    
    photo_db.name = photo_in.name
    photo_db.path = photo_in.path
    photo_db.user_id = decode_id(photo_in.user_id)
    photo_db.folder_id = decode_id(photo_in.folder_id)
    photo_db.is_active = photo_in.is_active

    db.add(photo_db)
    db.commit()
    db.refresh(photo_db)
    return photo_db

def delete_photo(photo_db: Photo, db: Session):
    # photo_service.delete_photo_from_minio(db,photo_db.path)
    db.delete(photo_db)
    db.commit()



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

def create_photo_entry(db: Session, name: str, user_id: str, folder_id: str, is_active: bool,user_id,file: UploadFile = File(...)):
    path = upload_image_to_minio(user_id,file)
    
    # Buscar la carpeta por ID
    folder = db.query(Folder).filter(
        Folder.id == decode_id(folder_id),
        Folder.is_active == True
    ).first()
    
    if not folder:
        raise FolderNotFoundError(folder_id=folder_id)
       
    photo_in = PhotoCreate(
        name=name,
        path=path,
        user_id=user_id,
        folder_id=folder_id,
        is_active=is_active
    )
    
    photo = create_photo(db, photo_in)
    
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




async def upload_image_to_minio(user_id,file: UploadFile = File(...)):


    if not file.content_type.startswith("image/"):
        raise FileNotValidate()

    user_id_int = decode_id(user_id)
    folder = f"usuario_{user_id_int}"
    filename = f"{file.filename}_{uuid4().hex}"
    path = f"{folder}/{filename}"

    bucket_name = os.getenv("MINIO_BUCKET", "fotos")


    minio_client = get_minio_client()
    minio_client.put_object(
        bucket_name,
        path,
        data=file.file, 
        length=-1,
        part_size=5 * 1024 * 1024,
        content_type=file.content_type
    )

    return path





###nuevo
from minio import Minio
from datetime import timedelta
from typing import Optional
from app.schemas.photo import PhotoResponse, PhotoListResponse
from app.repositories.photo_repository import PhotoRepository

from minio import Minio
from datetime import timedelta
from typing import Optional
from sqlalchemy.orm import Session
from app.schemas.photo import PhotoResponse, PhotoListResponse
from app.repositories.photo_repository import PhotoRepository

class PhotoService:
    def __init__(self, minio_client: Minio, bucket_name: str):
        self.minio_client = minio_client
        self.bucket_name = bucket_name

    def generate_presigned_url(self, object_path: str, expires_hours: int = 1) -> str:
        """Genera URL pre-firmada para acceso directo a MinIO"""
        try:
            url = self.minio_client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_path,
                expires=timedelta(hours=expires_hours)
            )
            return url
        except Exception as e:
            print(f"Error generando URL pre-firmada: {e}")
            return ""

    def get_list_photos(
        self, 
        db: Session,  
        user_id: int, 
        page: int = 1, 
        page_size: int = 20,
        folder_id: Optional[str] = None  # Cambio: ahora es str (hasheado)
    ) -> PhotoListResponse:
        """
        Método unificado que decide si traer por folder o por usuario
        """
        repo = PhotoRepository(db)
        
        if folder_id is not None:
            try:
                folder_id_int = decode_id(folder_id)
            except Exception:
                return PhotoListResponse(
                    photos=[],
                    total=0,
                    page=page,
                    page_size=page_size,
                    has_next=False
                )
            
            photos, total = repo.get_photos_by_folder(user_id, folder_id_int, page, page_size)
        else:
            photos, total = repo.get_photos_by_user(user_id, page, page_size)
        
        # Generar URLs pre-firmadas para cada foto
        photo_responses = []
        for photo in photos:
            signed_url = self.generate_presigned_url(photo.path)
            
            photo_response = PhotoResponse(
                id=photo.id,
                name=photo.name,
                path=photo.path,
                user_id=photo.user_id,
                folder_id=photo.folder_id,
                date=photo.date,
                signed_url=signed_url
            )
            photo_responses.append(photo_response)
        
        # Calcular si hay más páginas
        has_next = (page * page_size) < total
        
        # Retornar respuesta completa
        return PhotoListResponse(
            photos=photo_responses,
            total=total,
            page=page,
            page_size=page_size,
            has_next=has_next
        )

    # Wrappers actualizados para manejar folder_id hasheado
    def get_photos_by_folder(self, db: Session, user_id: int, folder_id: str, page: int = 1, page_size: int = 20):
        """Wrapper para compatibilidad - ahora recibe folder_id hasheado"""
        return self.get_list_photos(db, user_id, page, page_size, folder_id)

    def get_photos_by_user(self, db: Session, user_id: int, page: int = 1, page_size: int = 20):
        """Wrapper para compatibilidad"""
        return self.get_list_photos(db, user_id, page, page_size, None)

    def delete_photo_from_minio(self, db: Session, object_path: str):
        """Elimina un objeto del bucket de MinIO"""
        try:
            self.minio_client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_path
            )
            print(f"Archivo eliminado de MinIO: {object_path}")
        except Exception as e:
            print(f"Error al eliminar archivo de MinIO: {e}")