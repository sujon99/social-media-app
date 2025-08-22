from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.core.cache import cache
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Post, Comment
from .forms import PostForm, CommentForm
from .utils import upload_to_minio, delete_from_minio, get_minio_url
import os
import requests


@login_required
def serve_image_view(request, image_name):
    """Proxy view to serve MinIO images through Django"""
    try:
        # Get MinIO presigned URL
        minio_url = get_minio_url(image_name)
        if not minio_url:
            return HttpResponse("Image not found", status=404)
        
        # Fetch image from MinIO
        response = requests.get(minio_url, stream=True)
        if response.status_code != 200:
            return HttpResponse("Image not found", status=404)
        
        # Create Django response with proper headers
        django_response = HttpResponse(
            response.content,
            content_type=response.headers.get('content-type', 'image/jpeg')
        )
        
        # Set cache headers for better performance
        django_response['Cache-Control'] = 'public, max-age=3600'  # 1 hour cache
        
        return django_response
        
    except Exception as e:
        return HttpResponse("Error serving image", status=500)


@login_required
def create_post_view(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            
            # Handle image upload to MinIO
            if 'image' in request.FILES:
                image_file = request.FILES['image']
                # Save temporarily to handle MinIO upload
                import tempfile
                temp_fd, temp_path = tempfile.mkstemp(suffix=os.path.splitext(image_file.name)[1])
                with os.fdopen(temp_fd, 'wb') as destination:
                    for chunk in image_file.chunks():
                        destination.write(chunk)
                
                # Upload to MinIO
                minio_object_name = upload_to_minio(temp_path)
                if minio_object_name:
                    post.image = minio_object_name
                    # Clean up temp file
                    os.remove(temp_path)
                else:
                    os.remove(temp_path)
                    messages.error(request, 'Failed to upload image to MinIO. Please try again.')
                    return render(request, 'posts/create_post.html', {'form': form})
            
            post.save()
            messages.success(request, 'Post created successfully!')
            return redirect('post_list')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = PostForm()
    
    return render(request, 'posts/create_post.html', {'form': form})


@login_required
def post_list_view(request):
    # Verify session from Redis
    session_key = f"user_session_{request.user.id}"
    session_data = cache.get(session_key)
    
    if not session_data or not session_data.get('is_authenticated'):
        from django.contrib.auth import logout
        logout(request)
        messages.error(request, 'Session expired. Please login again.')
        return redirect('login')
    
    posts = Post.objects.select_related('author').prefetch_related('likes', 'comments').all()
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        posts = posts.filter(
            Q(title__icontains=search_query) |
            Q(content__icontains=search_query) |
            Q(author__username__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'search_query': search_query,
    }
    return render(request, 'posts/post_list.html', context)


@login_required
def post_detail_view(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.select_related('author').all()
    
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            messages.success(request, 'Comment added successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def like_post_view(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'like_count': post.like_count
        })
    
    return JsonResponse({'error': 'Invalid request method'})


@login_required
def edit_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            # Handle new image upload
            if 'image' in request.FILES:
                # Delete old image if it exists
                if post.image:
                    try:
                        # Convert ImageFieldFile to string for MinIO deletion
                        image_name = str(post.image)
                        delete_from_minio(image_name)
                    except:
                        pass  # Ignore deletion errors
                
                # Upload new image
                image_file = request.FILES['image']
                import tempfile
                temp_fd, temp_path = tempfile.mkstemp(suffix=os.path.splitext(image_file.name)[1])
                with os.fdopen(temp_fd, 'wb') as destination:
                    for chunk in image_file.chunks():
                        destination.write(chunk)
                
                # Upload to MinIO
                minio_object_name = upload_to_minio(temp_path)
                if minio_object_name:
                    post.image = minio_object_name
                    os.remove(temp_path)
                else:
                    os.remove(temp_path)
                    messages.error(request, 'Failed to upload image to MinIO. Please try again.')
                    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})
            
            form.save()
            messages.success(request, 'Post updated successfully!')
            return redirect('post_detail', post_id=post.id)
    else:
        form = PostForm(instance=post)
    
    return render(request, 'posts/edit_post.html', {'form': form, 'post': post})


@login_required
def delete_post_view(request, post_id):
    post = get_object_or_404(Post, id=post_id, author=request.user)
    
    if request.method == 'POST':
        # Delete image if it exists
        if post.image:
            try:
                # Convert ImageFieldFile to string for MinIO deletion
                image_name = str(post.image)
                delete_from_minio(image_name)
            except:
                pass  # Ignore deletion errors
        
        post.delete()
        messages.success(request, 'Post deleted successfully!')
        return redirect('post_list')
    
    return render(request, 'posts/delete_post.html', {'post': post})


@login_required
def my_posts_view(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'posts/my_posts.html', {'page_obj': page_obj}) 