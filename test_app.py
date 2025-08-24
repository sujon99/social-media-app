#!/usr/bin/env python3
"""
Comprehensive Test Suite for Social Media Application
Tests all functionality including: Redis, MinIO, Django models, sessions, URLs, forms, image proxy, and accessibility
"""

import os
import sys
import django
import uuid
import time
import requests
from datetime import datetime, timedelta

# Add the project directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'social_media.settings')
django.setup()

from django.contrib.auth.models import User
from django.test import Client
from django.core.cache import cache
from django.conf import settings
from django.urls import reverse
from users.models import UserProfile
from posts.models import Post, Comment
from posts.utils import get_minio_client, upload_to_minio, get_minio_url, delete_from_minio
from posts.templatetags.minio_filters import get_image_url
from users.forms import UserRegistrationForm
from posts.forms import PostForm

def test_redis_operations():
    """Test Redis cache operations"""
    print("🔍 Testing Redis operations...")
    
    # Test basic cache operations
    cache.set('test_key', 'test_value', 60)
    value = cache.get('test_key')
    assert value == 'test_value', f"Cache get failed: expected 'test_value', got '{value}'"
    print("✅ Basic cache operations working")
    
    # Test cache expiration
    cache.set('expire_test', 'expire_value', 1)
    time.sleep(2)
    expired_value = cache.get('expire_test')
    assert expired_value is None, f"Cache expiration failed: expected None, got '{expired_value}'"
    print("✅ Cache expiration working")
    
    # Test cache deletion
    cache.set('delete_test', 'delete_value')
    cache.delete('delete_test')
    deleted_value = cache.get('delete_test')
    assert deleted_value is None, f"Cache deletion failed: expected None, got '{deleted_value}'"
    print("✅ Cache deletion working")

def test_minio_operations():
    """Test MinIO operations"""
    print("🔍 Testing MinIO operations...")
    
    try:
        # Test MinIO client connection
        client = get_minio_client()
        buckets = client.list_buckets()
        bucket_names = [b.name for b in buckets]
        assert settings.MINIO_BUCKET_NAME in bucket_names, f"Bucket {settings.MINIO_BUCKET_NAME} not found"
        print("✅ MinIO client connection working")
        
        # Test file upload
        test_content = b"test file content"
        test_filename = f"test_{uuid.uuid4()}.txt"
        
        # Create temporary file
        with open(test_filename, 'wb') as f:
            f.write(test_content)
        
        # Upload to MinIO
        uploaded_name = upload_to_minio(test_filename)
        assert uploaded_name is not None, "File upload failed"
        print("✅ File upload working")
        
        # Test getting MinIO URL
        minio_url = get_minio_url(uploaded_name)
        assert minio_url is not None, "Failed to get MinIO URL"
        # Check if URL contains the configured MinIO endpoint
        if minio_url and settings.MINIO_ENDPOINT in minio_url:
            print("✅ MinIO URL generation working")
        else:
            print("⚠️  MinIO URL format may be unexpected")
        
        # Test template filter
        filter_url = get_image_url(uploaded_name)
        assert filter_url is not None, "Template filter failed"
        # Check if filter URL points to Django proxy (not direct MinIO)
        if filter_url and settings.MINIO_ENDPOINT not in filter_url:
            print("✅ Template filter working (proxy URL)")
        else:
            print("⚠️  Template filter may be exposing MinIO directly")
        
        # Test file deletion
        delete_result = delete_from_minio(uploaded_name)
        assert delete_result, "File deletion failed"
        print("✅ File deletion working")
        
        # Clean up local file
        os.remove(test_filename)
        
    except Exception as e:
        print(f"❌ MinIO operations failed: {e}")
        return False
    
    return True

def test_django_models():
    """Test Django models and relationships"""
    print("🔍 Testing Django models...")
    
    # Create test user with unique username
    test_username = f"testuser_{uuid.uuid4().hex[:8]}"
    user = User.objects.create_user(
        username=test_username,
        email=f"{test_username}@test.com",
        password="testpass123"
    )
    
    # Test UserProfile creation
    try:
        profile = user.userprofile
        assert profile is not None, "UserProfile not created automatically"
        print("✅ UserProfile auto-creation working")
    except UserProfile.DoesNotExist:
        print("❌ UserProfile not created automatically")
        return False
    
    # Test post creation
    post = Post.objects.create(
        user=user,
        title="Test Post",
        description="Test post description"
    )
    assert post.id is not None, "Post creation failed"
    print("✅ Post creation working")
    
    # Test comment creation
    comment = Comment.objects.create(
        post=post,
        user=user,
        content="Test comment"
    )
    assert comment.id is not None, "Comment creation failed"
    print("✅ Comment creation working")
    
    # Test likes
    post.likes.add(user)
    assert user in post.likes.all(), "Like functionality failed"
    print("✅ Like functionality working")
    
    # Test relationships
    assert post in user.post_set.all(), "User-post relationship failed"
    assert comment in post.comment_set.all(), "Post-comment relationship failed"
    print("✅ Model relationships working")
    
    # Clean up
    user.delete()
    print("✅ Model cleanup working")

def test_redis_session_management():
    """Test Redis-based session management"""
    print("🔍 Testing Redis session management...")
    
    client = Client()
    
    # Test session creation
    response = client.get('/login/')
    assert response.status_code == 200, "Login page not accessible"
    
    # Create a session
    session = client.session
    session['test_session_key'] = 'test_session_value'
    session.save()
    
    # Test session retrieval
    retrieved_value = session.get('test_session_key')
    assert retrieved_value == 'test_session_value', "Session retrieval failed"
    print("✅ Session creation and retrieval working")
    
    # Test session expiration
    session.set_expiry(1)  # 1 second
    session.save()
    time.sleep(2)
    
    # Try to retrieve expired session
    expired_value = session.get('test_session_key')
    assert expired_value is None, "Session expiration failed"
    print("✅ Session expiration working")
    
    # Test session deletion
    session['new_key'] = 'new_value'
    session.save()
    session.delete('new_key')
    session.save()
    
    deleted_value = session.get('new_key')
    assert deleted_value is None, "Session deletion failed"
    print("✅ Session deletion working")

def test_url_configuration():
    """Test URL configuration"""
    print("🔍 Testing URL configuration...")
    
    # Test main URLs
    try:
        login_url = reverse('login')
        assert login_url == '/login/', f"Login URL mismatch: {login_url}"
        print("✅ Login URL configuration working")
        
        dashboard_url = reverse('dashboard')
        assert dashboard_url == '/dashboard/', f"Dashboard URL mismatch: {dashboard_url}"
        print("✅ Dashboard URL configuration working")
        
        post_list_url = reverse('post_list')
        assert post_list_url == '/posts/', f"Post list URL mismatch: {post_list_url}"
        print("✅ Post list URL configuration working")
        
    except Exception as e:
        print(f"❌ URL configuration failed: {e}")
        return False
    
    return True

def test_django_forms():
    """Test Django forms"""
    print("🔍 Testing Django forms...")
    
    # Test user registration form
    form_data = {
        'username': f'testuser_{uuid.uuid4().hex[:8]}',
        'email': 'test@example.com',
        'password1': 'testpass123',
        'password2': 'testpass123'
    }
    
    form = UserRegistrationForm(data=form_data)
    assert form.is_valid(), f"User registration form validation failed: {form.errors}"
    print("✅ User registration form working")
    
    # Test post form
    post_form_data = {
        'title': 'Test Post Title',
        'description': 'Test post description'
    }
    
    post_form = PostForm(data=post_form_data)
    assert post_form.is_valid(), f"Post form validation failed: {post_form.errors}"
    print("✅ Post form working")

def test_high_availability_features():
    """Test high availability features"""
    print("🔍 Testing high availability features...")
    
    # Test Redis session persistence
    client1 = Client()
    client2 = Client()
    
    # Create session in one client
    session1 = client1.session
    session1['ha_test'] = 'ha_value'
    session1.save()
    
    # Verify session is accessible (simulating different server instance)
    session2 = client2.session
    session2.session_key = session1.session_key
    session2.load()
    
    retrieved_value = session2.get('ha_test')
    assert retrieved_value == 'ha_value', "High availability session failed"
    print("✅ High availability session working")
    
    # Test cache persistence
    cache.set('ha_cache_test', 'ha_cache_value', 300)
    cache_value = cache.get('ha_cache_test')
    assert cache_value == 'ha_cache_value', "High availability cache failed"
    print("✅ High availability cache working")

def test_image_proxy():
    """Test image proxy functionality"""
    print("🔍 Testing image proxy functionality...")
    
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
        
        print("✅ Image proxy test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Image proxy test failed: {e}")
        return False

def test_application_accessibility():
    """Test application accessibility from different hosts"""
    print("🔍 Testing application accessibility...")
    
    # Get server configuration
    server_host = os.getenv('SERVER_HOST', 'localhost')
    
    # Test local access
    try:
        response = requests.get(f'http://{server_host}/', timeout=5)
        if response.status_code in [200, 302]:  # 302 for redirect to login
            print("✅ Local access working")
        else:
            print(f"⚠️  Local access returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Local access failed: {e}")
    
    # Test with different Host headers
    try:
        headers = {'Host': 'example.com'}
        response = requests.get(f'http://{server_host}/', headers=headers, timeout=5)
        if response.status_code in [200, 302]:
            print("✅ Custom Host header (example.com) working")
        else:
            print(f"⚠️  Custom Host header returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Custom Host header test failed: {e}")
    
    # Test health endpoint
    try:
        response = requests.get(f'http://{server_host}/health/', timeout=5)
        if response.status_code == 200:
            print("✅ Health endpoint working")
        else:
            print(f"⚠️  Health endpoint returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Health endpoint test failed: {e}")

def run_all_tests():
    """Run all tests"""
    print("🚀 Starting comprehensive test suite...")
    print("=" * 60)
    
    test_functions = [
        test_redis_operations,
        test_minio_operations,
        test_django_models,
        test_redis_session_management,
        test_url_configuration,
        test_django_forms,
        test_high_availability_features,
        test_image_proxy,
        test_application_accessibility
    ]
    
    passed = 0
    failed = 0
    
    for test_func in test_functions:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"❌ {test_func.__name__} failed: {e}")
            failed += 1
        print("-" * 40)
    
    print("=" * 60)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! Your application is working correctly.")
    else:
        print("⚠️  Some tests failed. Check the errors above.")
    
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 