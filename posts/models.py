from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.cache import cache
import uuid
import os


class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.title} by {self.author.username}"
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comments.count()
    
    def save(self, *args, **kwargs):
        # If this is a new post with an image, we'll handle MinIO upload in the view
        super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # Delete image if it exists
        if self.image:
            try:
                from .utils import delete_from_minio
                # Convert ImageFieldFile to string for MinIO deletion
                image_name = str(self.image)
                delete_from_minio(image_name)
            except:
                pass  # Ignore deletion errors
        super().delete(*args, **kwargs)


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}" 