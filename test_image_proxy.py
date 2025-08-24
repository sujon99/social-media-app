#!/usr/bin/env python3
"""
Test script for image proxy functionality
"""

import os
import sys
import django
import tempfile
import uuid

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')
django.setup()

from django.conf import settings
from posts.utils import upload_to_minio, get_minio_url, delete_from_minio
from posts.templatetags.minio_filters import get_image_url

def test_image_proxy():
    """Test the image proxy functionality"""
    print("🔍 Testing Image Proxy Functionality")
    print("=" * 40)
    
    try:
        # Create a test image file
        test_content = b'fake image data for testing'
        test_filename = f"test_image_{uuid.uuid4()}.jpg"
        
        with open(test_filename, 'wb') as f:
            f.write(test_content)
        
        print(f"📁 Created test file: {test_filename}")
        
        # Upload to MinIO
        print("📤 Uploading to MinIO...")
        uploaded_name = upload_to_minio(test_filename)
        
        if not uploaded_name:
            print("❌ Upload failed")
            return False
        
        print(f"✅ Uploaded as: {uploaded_name}")
        
        # Test MinIO URL generation
        print("🔗 Testing MinIO URL generation...")
        minio_url = get_minio_url(uploaded_name)
        
        if not minio_url:
            print("❌ MinIO URL generation failed")
            return False
        
        print(f"✅ MinIO URL: {minio_url}")
        
        # Test template filter (proxy URL)
        print("🌐 Testing template filter (proxy URL)...")
        filter_url = get_image_url(uploaded_name)
        
        if not filter_url:
            print("❌ Template filter failed")
            return False
        
        print(f"✅ Proxy URL: {filter_url}")
        
        # Check if proxy URL is different from MinIO URL
        if filter_url != minio_url:
            print("✅ Proxy URL is different from MinIO URL (good!)")
        else:
            print("⚠️  Proxy URL is same as MinIO URL")
        
        # Check if MinIO endpoint is hidden in proxy URL
        if settings.MINIO_ENDPOINT not in filter_url:
            print("✅ MinIO endpoint is hidden in proxy URL (secure!)")
        else:
            print("❌ MinIO endpoint is exposed in proxy URL")
            return False
        
        # Clean up
        print("🧹 Cleaning up...")
        delete_result = delete_from_minio(uploaded_name)
        if delete_result:
            print("✅ File deleted from MinIO")
        else:
            print("⚠️  Failed to delete file from MinIO")
        
        # Remove local file
        os.remove(test_filename)
        print("✅ Local file removed")
        
        print("\n🎉 Image proxy test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_image_proxy()
    sys.exit(0 if success else 1)