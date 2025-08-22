from django.conf import settings
from minio import Minio
from minio.error import S3Error
import os
import uuid


def get_minio_client():
    """Get MinIO client instance"""
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ACCESS_KEY,
        secret_key=settings.MINIO_SECRET_KEY,
        secure=settings.MINIO_USE_HTTPS
    )


def ensure_bucket_exists():
    """Ensure the MinIO bucket exists"""
    try:
        client = get_minio_client()
        if not client.bucket_exists(settings.MINIO_BUCKET_NAME):
            client.make_bucket(settings.MINIO_BUCKET_NAME)
            print(f"Created bucket: {settings.MINIO_BUCKET_NAME}")
    except S3Error as e:
        print(f"Error ensuring bucket exists: {e}")


def upload_to_minio(file_path, object_name=None):
    """Upload a file to MinIO"""
    try:
        client = get_minio_client()
        ensure_bucket_exists()
        
        if object_name is None:
            object_name = os.path.basename(file_path)
        
        # Generate unique object name to avoid conflicts
        file_extension = os.path.splitext(object_name)[1]
        unique_object_name = f"{uuid.uuid4()}{file_extension}"
        
        client.fput_object(
            settings.MINIO_BUCKET_NAME,
            unique_object_name,
            file_path
        )
        
        return unique_object_name
    except S3Error as e:
        print(f"Error uploading to MinIO: {e}")
        return None


def delete_from_minio(object_name):
    """Delete a file from MinIO"""
    try:
        client = get_minio_client()
        client.remove_object(settings.MINIO_BUCKET_NAME, object_name)
        return True
    except S3Error as e:
        print(f"Error deleting from MinIO: {e}")
        return False


def get_minio_url(object_name):
    """Get the URL for a file stored in MinIO"""
    try:
        client = get_minio_client()
        from datetime import timedelta
        return client.presigned_get_object(
            settings.MINIO_BUCKET_NAME,
            object_name,
            expires=timedelta(hours=1)  # 1 hour
        )
    except S3Error as e:
        print(f"Error getting MinIO URL: {e}")
        return None 