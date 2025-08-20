from minio import Minio
import os

from datetime import timedelta
from sqlalchemy.orm import Session
from typing import Optional

from app.schemas.photo import PhotoListResponse,PhotoResponse

def get_minio_client():
    minio_client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT", "http://minio:9000/").replace("http://", ""),
    access_key=os.getenv("MINIO_ROOT_USER", "minio"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minio123"),
    secure=False
)
    return minio_client


# class PhotoServiceMinio:
#     def __init__(self, minio_client: Minio, bucket_name: str):
#         self.minio_client = minio_client
#         self.bucket_name = bucket_name

#     def generate_presigned_url(self, object_path: str, expires_hours: int = 1) -> str:
#         """Genera URL pre-firmada para acceso directo a MinIO"""
#         try:
#             url = self.minio_client.presigned_get_object(
#                 bucket_name=self.bucket_name,
#                 object_name=object_path,
#                 expires=timedelta(hours=expires_hours)
#             )
#             return url
#         except Exception as e:
#             print(f"Error generando URL pre-firmada: {e}")
#             return ""

#     def get_photos_by_folder(
#         self, 
#         db: Session,
#         user_id: int, 
#         folder_id: int, 
#         page: int = 1, 
#         page_size: int = 20
#     ) -> PhotoListResponse:
#         """Servicio para obtener fotos por folder"""
#         repo = PhotoRepository(db)
#         photos, total = repo.get_photos_by_folder(user_id, folder_id, page, page_size)
        
#         # Generar URLs pre-firmadas
#         photo_responses = []
#         for photo in photos:
#             signed_url = self.generate_presigned_url(photo.path)
#             photo_response = PhotoResponse(
#                 id=photo.id,
#                 name=photo.name,
#                 path=photo.path,
#                 user_id=photo.user_id,
#                 folder_id=photo.folder_id,
#                 date=photo.date,
#                 signed_url=signed_url
#             )
#             photo_responses.append(photo_response)
        
#         has_next = (page * page_size) < total
        
#         return PhotoListResponse(
#             photos=photo_responses,
#             total=total,
#             page=page,
#             page_size=page_size,
#             has_next=has_next
#         )

#     def get_photos_by_user(
#         self, 
#         db: Session,
#         user_id: int, 
#         page: int = 1, 
#         page_size: int = 20
#     ) -> PhotoListResponse:
#         """Servicio para obtener todas las fotos de un usuario"""
#         repo = PhotoRepository(db)
#         photos, total = repo.get_photos_by_user(user_id, page, page_size)
        
#         # Generar URLs pre-firmadas
#         photo_responses = []
#         for photo in photos:
#             signed_url = self.generate_presigned_url(photo.path)
#             photo_response = PhotoResponse(
#                 id=photo.id,
#                 name=photo.name,
#                 path=photo.path,
#                 user_id=photo.user_id,
#                 folder_id=photo.folder_id,
#                 date=photo.date,
#                 signed_url=signed_url
#             )
#             photo_responses.append(photo_response)
        
#         has_next = (page * page_size) < total
        
#         return PhotoListResponse(
#             photos=photo_responses,
#             total=total,
#             page=page,
#             page_size=page_size,
#             has_next=has_next
#         )

#     def get_single_photo(
#         self, 
#         db: Session,
#         photo_id: int, 
#         user_id: int
#     ) -> Optional[PhotoResponse]:
#         """Servicio para obtener una foto específica"""
#         repo = PhotoRepository(db)
#         photo = repo.get_photo_by_id(photo_id, user_id)
        
#         if not photo:
#             return None
        
#         signed_url = self.generate_presigned_url(photo.path)
        
#         return PhotoResponse(
#             id=photo.id,
#             name=photo.name,
#             path=photo.path,
#             user_id=photo.user_id,
#             folder_id=photo.folder_id,
#             date=photo.date,
#             signed_url=signed_url
#         )
    
    
