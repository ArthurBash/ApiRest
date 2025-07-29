from minio import Minio
import os



def get_minio_client():
    minio_client = Minio(
    endpoint=os.getenv("MINIO_ENDPOINT", "minio:9000").replace("http://", ""),
    access_key=os.getenv("MINIO_ROOT_USER", "minio"),
    secret_key=os.getenv("MINIO_ROOT_PASSWORD", "minio123"),
    secure=False
)
    return minio_client

# bucket_name = os.getenv("MINIO_BUCKET", "fotos")
