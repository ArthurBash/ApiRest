from sqlalchemy.orm import Session
from app.models.photo import Photo as PhotoModel
from app.schemas.photo import PhotoCreate,PhotoRead
from app.models.photo import Photo
from fastapi import  Depends,Path,HTTPException,UploadFile

from app.api.deps import get_db
from app.schemas.photo import PhotoUpdate, PhotoUpdatePUT



from app.exceptions import ErrorDecodificacion,ErrorFotoNoEncontrada
#from passlib.context import CryptContext

from hashids import Hashids
import os
from dotenv import load_dotenv

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

def delete_photo(photo_db: Photo,db: Session):
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



# async def upload_photo(file: UploadFile):
#     try:
#         content = await file.read()

#         filename = f"{uuid.uuid4()}_{file.filename}"

#         s3.put_object(
#             Bucket=BUCKET_NAME,
#             Key=filename,
#             Body=content,
#             ContentType=file.content_type
#         )

#         return {
#             "message": "Imagen subida con éxito",
#             "filename": filename,
#             "url": f"http://{MINIO_ENDPOINT}/{BUCKET_NAME}/{filename}"
#         }

#     except Exception as e:
#         raise HTTPException(status_code=500, detail=str(e))

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


async def upload_image_to_minio(file: UploadFile = File(...)):
    if not file.content_type.startswith("image/"):
        raise HTTPException(status_code=400, detail="Archivo no es una imagen válida")

#    # Validación de tamaño
#     if file.content_type > 5 * 1024 * 1024:  # 5MB
#         raise HTTPException(status_code=400, detail="Archivo demasiado grande")


    # Generar path aleatorio
    # folder = uuid4().hex[:8]      # ejemplo: '9a3b2f1d
    folder = "fotos_prueba"
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