from fastapi import Depends, HTTPException, status,Path
from sqlalchemy.orm import Session

from app.db.session import SessionLocal

from app.services.minio_client import get_minio_client
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_photo_service():
    from app.services.photo import PhotoService
    """
    Crea y retorna una instancia del PhotoService con MinIO configurado
    Esta función será inyectada por FastAPI en tus controladores
    """
    minio_client = get_minio_client()
   # bucket_name = get_bucket_name()
    
    return PhotoService(
        minio_client=minio_client,
        bucket_name="fotos"
    )