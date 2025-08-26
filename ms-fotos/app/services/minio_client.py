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

