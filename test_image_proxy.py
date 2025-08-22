#!/usr/bin/env python3
"""
Test image proxy functionality
"""

import os
import sys
import django

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')
django.setup()

from posts.templatetags.minio_filters import get_image_url
from posts.utils import upload_to_minio
import tempfile

def test_image_proxy():
    """Test image proxy functionality"""
    print("Testing image proxy functionality...")
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
        temp_file.write(b'fake image data')
        temp_path = temp_file.name
    
    try:
        # Test upload to MinIO
        print("1. Testing image upload to MinIO...")
        object_name = upload_to_minio(temp_path)
        if object_name:
            print(f"   ✓ Upload successful: {object_name}")
        else:
            print("   ✗ Upload failed")
            return False
        
        # Test template filter (should return Django URL, not MinIO URL)
        print("2. Testing template filter...")
        # Create a mock ImageField object
        class MockImageField:
            def __str__(self):
                return object_name
        
        mock_image = MockImageField()
        filter_url = get_image_url(mock_image)
        if filter_url:
            print(f"   ✓ Template filter working: {filter_url}")
            # Check that it's a Django URL, not MinIO URL
            if '192.168.91.110:9000' not in filter_url:
                print("   ✓ URL is Django URL (MinIO server hidden)")
            else:
                print("   ✗ URL still contains MinIO server details")
                return False
        else:
            print("   ✗ Template filter failed")
            return False
        
        # Clean up
        from posts.utils import delete_from_minio
        delete_from_minio(object_name)
        
        print("\n🎉 Image proxy test passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during testing: {e}")
        return False
    finally:
        # Clean up temp file
        if os.path.exists(temp_path):
            os.unlink(temp_path)

if __name__ == "__main__":
    test_image_proxy()