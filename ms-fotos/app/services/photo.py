from sqlalchemy.orm import Session
from app.models.photo import Photo as PhotoModel
from app.schemas.photo import PhotoCreate,PhotoRead
from app.models.photo import Photo
from fastapi import  Depends,Path,HTTPException,UploadFile

from app.api.deps import get_db
from app.schemas.photo import PhotoUpdate, PhotoUpdatePUT

from minio import Minio


from app.exceptions import ErrorDecodificacion,ErrorFotoNoEncontrada
#from passlib.context import CryptContext

from hashids import Hashids
import os
from dotenv import load_dotenv

from fastapi.responses import StreamingResponse


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
    try:
        decoded_id = decode_id(photo_id)
    except Exception:
        raise ErrorDecodificacion()

    photo = db.query(Photo).filter_by(id=decoded_id).first()

    if not photo:
        raise ErrorFotoNoEncontrada()
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

def create_photo_entry(db: Session, name: str, path: str, user_id: str, folder_id: str, is_active: bool):
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


def descargar_archivos_de_usuario(
    db: Session,
    bucket_name: str,
    user_id: str,
    destino_local: str = "/tmp/fotos"
):
    client = get_minio_client()

    # Fotos de ese usuario
    fotos = db.query(Photo).filter(Photo.user_id == user_id).all()
    if not fotos:
        return []

    # Obtener prefijos
    prefijos = set()
    for foto in fotos:
        prefijo = os.path.dirname(foto.path).lstrip("/") + "/"  # quitar '/' inicial
        prefijos.add(prefijo)

    archivos_descargados = []

    for prefijo in prefijos:
        objetos = client.list_objects(bucket_name, prefix=prefijo, recursive=True)
        for obj in objetos:
            relative_path = obj.object_name[len(prefijo):]
            ruta_local = os.path.join(destino_local, prefijo, relative_path)
            os.makedirs(os.path.dirname(ruta_local), exist_ok=True)
            client.fget_object(bucket_name, obj.object_name, ruta_local)
            archivos_descargados.append(obj.object_name)

    return archivos_descargados




async def upload_image_to_minio(user_id,file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Archivo no es una imagen válida")

#    # Validación de tamaño
#     if file.content_type > 5 * 1024 * 1024:  # 5MB
#         raise HTTPException(status_code=400, detail="Archivo demasiado grande")


    # Generar path aleatorio
    # folder = uuid4().hex[:8]      # ejemplo: '9a3b2f1d
    print(f"-------------------{user_id}")
    user_id_int = decode_id(user_id)
    folder = f"usuario_{user_id_int}"
    filename = f"{file.filename}_{uuid4().hex}"
    path = f"{folder}/{filename}"

    bucket_name = os.getenv("MINIO_BUCKET", "fotos")


    minio_client = get_minio_client()
    # Subir a MinIO
    minio_client.put_object(
        bucket_name,
        path,
        data=file.file, 
        length=-1,
        part_size=5 * 1024 * 1024,
        content_type=file.content_type
    )

    # Registrar path en tu modelo/PostgreSQL
    # insert_path_to_db(path)  <-- ya lo tenés funcionando

    return path

def descargar_fotos_usuarios(user_id):
    id_real = decode_id(photo_id)
    foto = db.query(Photo).filter(Photo.id == id_real).first()
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return stream_photo_from_minio("fotos",foto.path.lstrip("/"))

def stream_photo_from_minio(bucket_name: str, object_name: str):
    client = get_minio_client()
    response = client.get_object(bucket_name, object_name)
    return StreamingResponse(response, media_type="image/jpeg")  # o detectarlo dinámicamente




###nuevo
from minio import Minio
from datetime import timedelta
from typing import Optional
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
        folder_id: Optional[int] = None  #
    ) -> PhotoListResponse:
        """
        Método unificado que decide si traer por folder o por usuario
        """
        # Crear el repository con la sesión de BD
        repo = PhotoRepository(db)
        
        # Decidir qué método usar según si hay folder_id
        if folder_id is not None:
            photos, total = repo.get_photos_by_folder(user_id, folder_id, page, page_size)
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

    # Mantén los métodos específicos si los necesitas en otros lugares
    def get_photos_by_folder(self, db: Session, user_id: int, folder_id: int, page: int = 1, page_size: int = 20):
        """Wrapper para compatibilidad"""
        return self.get_list_photos(db, user_id, page, page_size, folder_id)

    def get_photos_by_user(self, db: Session, user_id: int, page: int = 1, page_size: int = 20):
        """Wrapper para compatibilidad"""
        return self.get_list_photos(db, user_id, page, page_size, None)

    
 

    def delete_photo_from_minio(self, db: Session,object_path: str):
        """Elimina un objeto del bucket de MinIO"""
        try:
            self.minio_client.remove_object(
                bucket_name=self.bucket_name,
                object_name=object_path
            )
            print(f"Archivo eliminado de MinIO: {object_path}")
        except Exception as e:
            print(f"Error al eliminar archivo de MinIO: {e}")
