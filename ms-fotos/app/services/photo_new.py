
# services/photo_service.py
from typing import List
from repositories.photo_repository import PhotoRepository
from repositories.folder_repository import FolderRepository
from schemas.photo_schemas import PhotoCreate, PhotoUpdate, PhotoResponse
from exceptions import PhotoNotFoundError, FolderNotFoundError, FileNotValidate
from utils.hashids_utils import encode_id, decode_id
from services.minio_service import MinioService
from pathlib import Path


class PhotoService:
    def __init__(self, photo_repository: PhotoRepository, folder_repository: FolderRepository, minio_service: MinioService):
        self.photo_repository = photo_repository
        self.folder_repository = folder_repository
        self.minio_service = minio_service

    def create_photo(self, photo_data: PhotoCreate, file_content: bytes = None) -> PhotoResponse:
        """Crear una nueva foto y subirla a MinIO"""
        # Decodificar folder_id
        folder_id = decode_id(photo_data.folder_id)
        
        # Validar que el folder existe
        folder = self.folder_repository.get_by_id(folder_id)
        if not folder:
            raise FolderNotFoundError(folder_id=photo_data.folder_id)
        
        # Validar extensión
        allowed_extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp'}
        file_extension = Path(photo_data.name).suffix.lower()
        if file_extension not in allowed_extensions:
            raise FileNotValidate(f"Extensión {file_extension} no permitida")
        
        # Generar path único en MinIO
        minio_path = f"folders/{folder.name}/{photo_data.name}"
        
        # Validar que el path no existe
        if self.photo_repository.exists_by_path(minio_path):
            raise ValueError("Ya existe una foto con este nombre en la carpeta")
        
        # Subir archivo a MinIO si se proporciona contenido
        if file_content:
            self.minio_service.upload_file(minio_path, file_content)
        
        # Crear registro en BD
        photo_dict = {
            "name": photo_data.name,
            "path": minio_path,
            "user_id": photo_data.user_id,
            "folder_id": folder_id
        }
        
        photo = self.photo_repository.create(photo_dict)
        
        photo_response = PhotoResponse.model_validate(photo)
        photo_response.id = encode_id(photo.id)
        photo_response.folder_id = photo_data.folder_id  # Devolver hasheado
        return photo_response

    def get_photo_by_id(self, photo_hash_id: str) -> PhotoResponse:
        """Obtener foto por ID hasheado"""
        photo_id = decode_id(photo_hash_id)
        photo = self.photo_repository.get_by_id(photo_id)
        if not photo:
            raise PhotoNotFoundError(f"Photo con ID {photo_hash_id} no fue encontrada")
        
        photo_response = PhotoResponse.model_validate(photo)
        photo_response.id = photo_hash_id
        photo_response.folder_id = encode_id(photo.folder_id)
        return photo_response

    def get_presigned_url(self, photo_hash_id: str, expiration: int = 3600) -> str:
        """Generar URL pre-firmada para acceso directo a MinIO"""
        photo_id = decode_id(photo_hash_id)
        photo = self.photo_repository.get_by_id(photo_id)
        if not photo:
            raise PhotoNotFoundError(f"Photo con ID {photo_hash_id} no fue encontrada")
        
        return self.minio_service.get_presigned_url(photo.path, expiration)

    def get_photos_by_folder(self, folder_hash_id: str, skip: int = 0, limit: int = 100) -> List[PhotoResponse]:
        """Obtener fotos por carpeta"""
        folder_id = decode_id(folder_hash_id)
        
        # Validar que el folder existe
        folder = self.folder_repository.get_by_id(folder_id)
        if not folder:
            raise FolderNotFoundError(folder_id=folder_hash_id)
        
        photos = self.photo_repository.get_by_folder_id(folder_id, skip=skip, limit=limit)
        photo_responses = []
        
        for photo in photos:
            photo_response = PhotoResponse.model_validate(photo)
            photo_response.id = encode_id(photo.id)
            photo_response.folder_id = folder_hash_id
            photo_responses.append(photo_response)
        
        return photo_responses

    def update_photo(self, photo_hash_id: str, photo_data: PhotoUpdate) -> PhotoResponse:
        """Actualizar foto"""
        photo_id = decode_id(photo_hash_id)
        
        # Validar que existe
        existing_photo = self.photo_repository.get_by_id(photo_id)
        if not existing_photo:
            raise PhotoNotFoundError(f"Photo con ID {photo_hash_id} no fue encontrada")
        
        update_dict = {}
        
        # Validar folder_id si se está actualizando
        if photo_data.folder_id:
            folder_id = decode_id(photo_data.folder_id)
            folder = self.folder_repository.get_by_id(folder_id)
            if not folder:
                raise FolderNotFoundError(folder_id=photo_data.folder_id)
            update_dict["folder_id"] = folder_id
        
        # Agregar otros campos
        if photo_data.name:
            update_dict["name"] = photo_data.name
        if photo_data.user_id:
            update_dict["user_id"] = photo_data.user_id
        if photo_data.is_active is not None:
            update_dict["is_active"] = photo_data.is_active
        
        updated_photo = self.photo_repository.update(photo_id, update_dict)
        
        photo_response = PhotoResponse.model_validate(updated_photo)
        photo_response.id = photo_hash_id
        photo_response.folder_id = encode_id(updated_photo.folder_id)
        return photo_response

    def delete_photo(self, photo_hash_id: str) -> bool:
        """Eliminar foto (soft delete)"""
        photo_id = decode_id(photo_hash_id)
        
        # Obtener foto para eliminar de MinIO
        photo = self.photo_repository.get_by_id(photo_id)
        if photo:
            # Eliminar de MinIO
            self.minio_service.delete_file(photo.path)
        
        return self.photo_repository.soft_delete(photo_id)


# services/minio_service.py
import os
from minio import Minio
from minio.error import S3Error
from datetime import timedelta
from io import BytesIO


class MinioService:
    def __init__(self):
        self.client = Minio(
            endpoint=os.getenv("MINIO_ENDPOINT"),
            access_key=os.getenv("MINIO_ACCESS_KEY"),
            secret_key=os.getenv("MINIO_SECRET_KEY"),
            secure=os.getenv("MINIO_SECURE", "False").lower() == "true"
        )
        self.bucket_name = os.getenv("MINIO_BUCKET_NAME", "photos")
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self):
        """Crear bucket si no existe"""
        try:
            if not self.client.bucket_exists(self.bucket_name):
                self.client.make_bucket(self.bucket_name)
        except S3Error as e:
            print(f"Error creating bucket: {e}")

    def upload_file(self, object_name: str, file_content: bytes) -> bool:
        """Subir archivo a MinIO"""
        try:
            data = BytesIO(file_content)
            self.client.put_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                data=data,
                length=len(file_content)
            )
            return True
        except S3Error as e:
            print(f"Error uploading file: {e}")
            return False

    def get_presigned_url(self, object_name: str, expiration: int = 3600) -> str:
        """Generar URL pre-firmada"""
        try:
            url = self.client.presigned_get_object(
                bucket_name=self.bucket_name,
                object_name=object_name,
                expires=timedelta(seconds=expiration)
            )
            return url
        except S3Error as e:
            print(f"Error generating presigned URL: {e}")
            return None

    def delete_file(self, object_name: str) -> bool:
        """Eliminar archivo de MinIO"""
        try:
            self.client.remove_object(self.bucket_name, object_name)
            return True
        except S3Error as e:
            print(f"Error deleting file: {e}")
            return False