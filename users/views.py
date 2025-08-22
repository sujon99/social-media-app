from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.cache import cache
import json
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, 
    UserProfileForm, UserUpdateForm, CustomPasswordChangeForm
)
from .models import UserProfile


def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                # Store session info in Redis for high availability
                session_key = f"user_session_{user.id}"
                session_data = {
                    'user_id': user.id,
                    'username': user.username,
                    'is_authenticated': True
                }
                cache.set(session_key, session_data, timeout=3600)  # 1 hour
                
                messages.success(request, f'Welcome back, {user.username}!')
                return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})


@login_required
def logout_view(request):
    # Clear session from Redis
    session_key = f"user_session_{request.user.id}"
    cache.delete(session_key)
    
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')


@login_required
def dashboard_view(request):
    # Verify session from Redis
    session_key = f"user_session_{request.user.id}"
    session_data = cache.get(session_key)
    
    if not session_data or not session_data.get('is_authenticated'):
        logout(request)
        messages.error(request, 'Session expired. Please login again.')
        return redirect('login')
    
    # Get recent posts for the dashboard
    from posts.models import Post
    recent_posts = Post.objects.select_related('author').prefetch_related('likes', 'comments').order_by('-created_at')[:6]
    
    return render(request, 'users/dashboard.html', {
        'user': request.user,
        'recent_posts': recent_posts
    })


@login_required
def profile_view(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            
            # Handle profile picture upload to MinIO
            if 'profile_picture' in request.FILES:
                profile_picture = request.FILES['profile_picture']
                
                # Delete old profile picture if it exists
                if request.user.userprofile.profile_picture:
                    try:
                        from posts.utils import delete_from_minio
                        # Convert ImageFieldFile to string for MinIO deletion
                        old_image_name = str(request.user.userprofile.profile_picture)
                        delete_from_minio(old_image_name)
                    except:
                        pass  # Ignore deletion errors
                
                # Save temporarily to handle MinIO upload
                import tempfile
                import os
                temp_fd, temp_path = tempfile.mkstemp(suffix=os.path.splitext(profile_picture.name)[1])
                with os.fdopen(temp_fd, 'wb') as destination:
                    for chunk in profile_picture.chunks():
                        destination.write(chunk)
                
                # Upload to MinIO
                from posts.utils import upload_to_minio
                minio_object_name = upload_to_minio(temp_path)
                if minio_object_name:
                    # Update the profile picture field
                    profile_form.instance.profile_picture = minio_object_name
                    os.remove(temp_path)
                else:
                    os.remove(temp_path)
                    messages.error(request, 'Failed to upload profile picture to MinIO. Please try again.')
                    return render(request, 'users/profile.html', {
                        'user_form': user_form,
                        'profile_form': profile_form,
                    })
            
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
    }
    return render(request, 'users/profile.html', context)


@login_required
def change_password_view(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'users/change_password.html', {'form': form})


@csrf_exempt
def check_session_view(request):
    """API endpoint to check if user session is valid (for high availability)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_id = data.get('user_id')
            
            if user_id:
                session_key = f"user_session_{user_id}"
                session_data = cache.get(session_key)
                
                if session_data and session_data.get('is_authenticated'):
                    return JsonResponse({'valid': True, 'user': session_data})
                else:
                    return JsonResponse({'valid': False, 'message': 'Session expired'})
            else:
                return JsonResponse({'valid': False, 'message': 'User ID required'})
        except json.JSONDecodeError:
            return JsonResponse({'valid': False, 'message': 'Invalid JSON'})
    
    return JsonResponse({'valid': False, 'message': 'Invalid request method'})


def home_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'users/home.html') 