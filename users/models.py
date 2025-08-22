from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s profile"
    
    def delete(self, *args, **kwargs):
        # Delete profile picture from MinIO if it exists
        if self.profile_picture:
            try:
                from posts.utils import delete_from_minio
                # Convert ImageFieldFile to string for MinIO deletion
                image_name = str(self.profile_picture)
                delete_from_minio(image_name)
            except:
                pass  # Ignore deletion errors
        super().delete(*args, **kwargs)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Create UserProfile if it doesn't exist (for users created before UserProfile model)
        UserProfile.objects.create(user=instance) 