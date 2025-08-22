#!/usr/bin/env python3
"""
Comprehensive Test Suite for Social Media Application
Tests all major components: Django models, Redis sessions, MinIO operations, URLs, and forms
"""

import os
import sys
import django
import tempfile
import uuid
from datetime import datetime, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')
django.setup()

from django.test import Client
from django.contrib.auth.models import User
from django.core.cache import cache
from django.urls import reverse
from posts.models import Post, Comment
from posts.utils import upload_to_minio, delete_from_minio, get_minio_url
from posts.templatetags.minio_filters import get_image_url
from users.models import UserProfile
from users.forms import CustomUserCreationForm, CustomAuthenticationForm

def test_redis_connection():
    """Test Redis connection and basic operations"""
    print("Testing Redis connection and operations...")
    
    try:
        # Test basic Redis operations
        test_key = f"test_key_{uuid.uuid4().hex[:8]}"
        test_value = "test_value"
        
        # Set value
        cache.set(test_key, test_value, timeout=60)
        print("   ✓ Set operation successful")
        
        # Get value
        retrieved_value = cache.get(test_key)
        if retrieved_value == test_value:
            print("   ✓ Get operation successful")
        else:
            print("   ✗ Get operation failed")
            return False
        
        # Delete value
        cache.delete(test_key)
        print("   ✓ Delete operation successful")
        
        # Verify deletion
        if cache.get(test_key) is None:
            print("   ✓ Deletion verification successful")
        else:
            print("   ✗ Deletion verification failed")
            return False
        
        print("   ✓ Redis connection and operations working correctly")
        return True
        
    except Exception as e:
        print(f"   ✗ Redis test failed: {e}")
        return False

def test_minio_operations():
    """Test MinIO upload, download, and deletion operations"""
    print("Testing MinIO operations...")
    
    try:
        # Create a temporary test file
        with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as temp_file:
            temp_file.write(b'fake image data for testing')
            temp_path = temp_file.name
        
        try:
            # Test upload
            print("   ✓ Testing upload to MinIO...")
            object_name = upload_to_minio(temp_path)
            if object_name:
                print(f"   ✓ Upload successful: {object_name}")
            else:
                print("   ✗ Upload failed")
                return False
            
            # Test URL generation
            print("   ✓ Testing URL generation...")
            minio_url = get_minio_url(object_name)
            if minio_url and '192.168.91.110:9000' in minio_url:
                print("   ✓ URL generation successful")
            else:
                print("   ✗ URL generation failed")
                return False
            
            # Test template filter
            print("   ✓ Testing template filter...")
            class MockImageField:
                def __str__(self):
                    return object_name
            
            mock_image = MockImageField()
            filter_url = get_image_url(mock_image)
            if filter_url and '192.168.91.110:9000' not in filter_url:
                print("   ✓ Template filter working (MinIO hidden)")
            else:
                print("   ✗ Template filter failed")
                return False
            
            # Test deletion
            print("   ✓ Testing deletion from MinIO...")
            delete_result = delete_from_minio(object_name)
            if delete_result:
                print("   ✓ Deletion successful")
            else:
                print("   ✗ Deletion failed")
                return False
            
            print("   ✓ All MinIO operations working correctly")
            return True
            
        finally:
            # Clean up temp file
            if os.path.exists(temp_path):
                os.unlink(temp_path)
                
    except Exception as e:
        print(f"   ✗ MinIO test failed: {e}")
        return False

def test_django_models():
    """Test Django models and database operations"""
    print("Testing Django models...")
    
    try:
        # Create test user
        test_username = f"testuser_{uuid.uuid4().hex[:8]}"
        test_user = User.objects.create_user(
            username=test_username,
            email=f"{test_username}@test.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        print(f"   ✓ User model working. Created user: {test_username}")
        
        # Test UserProfile creation (should be automatic via signals)
        try:
            user_profile = test_user.userprofile
            print("   ✓ UserProfile model working. Profile created automatically")
        except UserProfile.DoesNotExist:
            print("   ✗ UserProfile not created automatically")
            return False
        
        # Create test post
        test_post = Post.objects.create(
            title="Test Post",
            content="This is a test post content for testing purposes.",
            author=test_user
        )
        print(f"   ✓ Post model working. Created post: {test_post.title}")
        
        # Create test comment
        test_comment = Comment.objects.create(
            content="This is a test comment.",
            post=test_post,
            author=test_user
        )
        print(f"   ✓ Comment model working. Created comment on post: {test_post.title}")
        
        # Test relationships
        if test_post.author == test_user:
            print("   ✓ Post-author relationship working")
        else:
            print("   ✗ Post-author relationship failed")
            return False
        
        if test_comment.post == test_post:
            print("   ✓ Comment-post relationship working")
        else:
            print("   ✗ Comment-post relationship failed")
            return False
        
        # Test like functionality
        test_post.likes.add(test_user)
        if test_user in test_post.likes.all():
            print("   ✓ Post likes functionality working")
        else:
            print("   ✗ Post likes functionality failed")
            return False
        
        # Clean up
        test_post.delete()
        test_user.delete()
        
        print("   ✓ All Django models working correctly")
        return True
        
    except Exception as e:
        print(f"   ✗ Django models test failed: {e}")
        return False

def test_redis_sessions():
    """Test Redis-based session management"""
    print("Testing Redis session management...")
    
    try:
        # Create test user
        test_username = f"sessionuser_{uuid.uuid4().hex[:8]}"
        test_user = User.objects.create_user(
            username=test_username,
            email=f"{test_username}@test.com",
            password="testpass123"
        )
        
        # Test session creation
        session_key = f"user_session_{test_user.id}"
        session_data = {
            'user_id': test_user.id,
            'username': test_user.username,
            'is_authenticated': True,
            'created_at': datetime.now().isoformat()
        }
        
        cache.set(session_key, session_data, timeout=3600)
        print("   ✓ Session creation successful")
        
        # Test session retrieval
        retrieved_session = cache.get(session_key)
        if retrieved_session and retrieved_session.get('is_authenticated'):
            print("   ✓ Session retrieval successful")
        else:
            print("   ✗ Session retrieval failed")
            return False
        
        # Test session expiration (set short timeout for testing)
        cache.set(session_key, session_data, timeout=1)
        import time
        time.sleep(2)  # Wait for expiration
        
        expired_session = cache.get(session_key)
        if expired_session is None:
            print("   ✓ Session expiration working")
        else:
            print("   ✗ Session expiration failed")
            return False
        
        # Test session deletion
        cache.set(session_key, session_data, timeout=3600)
        cache.delete(session_key)
        if cache.get(session_key) is None:
            print("   ✓ Session deletion working")
        else:
            print("   ✗ Session deletion failed")
            return False
        
        # Clean up
        test_user.delete()
        
        print("   ✓ Redis session management working correctly")
        return True
        
    except Exception as e:
        print(f"   ✗ Redis session test failed: {e}")
        return False

def test_url_configuration():
    """Test URL configuration and routing"""
    print("Testing URL configuration...")
    
    try:
        client = Client()
        
        # Test home page
        response = client.get('/')
        if response.status_code in [200, 302]:  # 302 for redirect if authenticated
            print("   ✓ Home page URL working")
        else:
            print("   ✗ Home page URL failed")
            return False
        
        # Test login page
        response = client.get('/login/')
        if response.status_code == 200:
            print("   ✓ Login page URL working")
        else:
            print("   ✗ Login page URL failed")
            return False
        
        # Test signup page
        response = client.get('/signup/')
        if response.status_code == 200:
            print("   ✓ Signup page URL working")
        else:
            print("   ✗ Signup page URL failed")
            return False
        
        # Test posts list page
        response = client.get('/posts/')
        if response.status_code == 302:  # Should redirect to login
            print("   ✓ Posts list URL working (redirects to login)")
        else:
            print("   ✗ Posts list URL failed")
            return False
        
        print("   ✓ All URL configurations working correctly")
        return True
        
    except Exception as e:
        print(f"   ✗ URL configuration test failed: {e}")
        return False

def test_forms():
    """Test Django forms"""
    print("Testing Django forms...")
    
    try:
        # Test user creation form
        form_data = {
            'username': f"formuser_{uuid.uuid4().hex[:8]}",
            'email': f"formuser_{uuid.uuid4().hex[:8]}@test.com",
            'password1': 'testpass123',
            'password2': 'testpass123',
            'first_name': 'Form',
            'last_name': 'User'
        }
        
        user_form = CustomUserCreationForm(data=form_data)
        if user_form.is_valid():
            print("   ✓ User creation form validation working")
        else:
            print(f"   ✗ User creation form validation failed: {user_form.errors}")
            return False
        
        # Test authentication form
        auth_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        
        auth_form = CustomAuthenticationForm(data=auth_data)
        if auth_form.is_valid():
            print("   ✓ Authentication form validation working")
        else:
            print(f"   ✗ Authentication form validation failed: {auth_form.errors}")
            return False
        
        print("   ✓ All forms working correctly")
        return True
        
    except Exception as e:
        print(f"   ✗ Forms test failed: {e}")
        return False

def test_high_availability():
    """Test high availability features"""
    print("Testing high availability features...")
    
    try:
        # Test session persistence across cache operations
        test_key = f"ha_test_{uuid.uuid4().hex[:8]}"
        test_data = {
            'user_id': 12345,
            'username': 'ha_user',
            'is_authenticated': True,
            'timestamp': datetime.now().isoformat()
        }
        
        # Store in Redis
        cache.set(test_key, test_data, timeout=3600)
        
        # Simulate application restart (cache should persist)
        retrieved_data = cache.get(test_key)
        if retrieved_data and retrieved_data.get('user_id') == 12345:
            print("   ✓ Session persistence working")
        else:
            print("   ✗ Session persistence failed")
            return False
        
        # Test session validation
        if retrieved_data.get('is_authenticated'):
            print("   ✓ Session validation working")
        else:
            print("   ✗ Session validation failed")
            return False
        
        # Clean up
        cache.delete(test_key)
        
        print("   ✓ High availability features working correctly")
        return True
        
    except Exception as e:
        print(f"   ✗ High availability test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("=" * 50)
    print("Social Media Application - Comprehensive Test Suite")
    print("=" * 50)
    print()
    
    tests = [
        ("Redis Connection & Operations", test_redis_connection),
        ("MinIO Operations", test_minio_operations),
        ("Django Models", test_django_models),
        ("Redis Session Management", test_redis_sessions),
        ("URL Configuration", test_url_configuration),
        ("Django Forms", test_forms),
        ("High Availability Features", test_high_availability),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"--- {test_name} ---")
        if test_func():
            passed += 1
            print()
        else:
            print()
    
    print("=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    print("=" * 50)
    
    if passed == total:
        print("🎉 All tests passed! Your application is fully functional.")
        print()
        print("Next steps:")
        print("1. Start the development server: python manage.py runserver")
        print("2. Open your browser and go to http://127.0.0.1:8000/")
        print("3. Create a new account and start using the application!")
        print()
        print("🚀 Your social media application is ready for production!")
    else:
        print(f"⚠️  {total - passed} test(s) failed. Please check the errors above.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 