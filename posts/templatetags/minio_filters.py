from django import template
from django.urls import reverse
from django.conf import settings
import os

register = template.Library()

@register.filter
def get_image_url(image_field):
    """
    Get the Django URL for serving MinIO images.
    Images are proxied through Django to hide MinIO server details.
    """
    if not image_field:
        return None
    
    # Get the image name
    image_name = str(image_field)
    
    # Return Django URL that will proxy to MinIO
    try:
        return reverse('serve_image', kwargs={'image_name': image_name})
    except:
        return None 