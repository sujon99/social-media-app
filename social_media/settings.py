"""
Django settings for social_media project.
"""

from pathlib import Path
from decouple import config
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow any host - domain management handled by DNS/hosts file
ALLOWED_HOSTS = ['*']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders',
    'users',
    'posts',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'social_media.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'social_media.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': config('DATABASE_NAME', default='mydb'),
        'USER': config('DATABASE_USER', default='myuser'),
        'PASSWORD': config('DATABASE_PASSWORD', default='mypassword'),
        'HOST': config('DATABASE_HOST', default='localhost'),
        'PORT': config('DATABASE_PORT', default='3306'),
        'OPTIONS': {
            'charset': 'utf8mb4',
        },
    }
}

# Redis Configuration for Session Storage
CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': f"redis://{config('REDIS_HOST', default='localhost')}:{config('REDIS_PORT', default='6379')}/1",
        'OPTIONS': {
            'CLIENT_CLASS': 'django_redis.client.DefaultClient',
        }
    }
}

# Session Configuration
SESSION_ENGINE = 'django.contrib.sessions.backends.cache'
SESSION_CACHE_ALIAS = 'default'
SESSION_COOKIE_AGE = 3600  # 1 hour
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# Additional session settings for Docker environment
SESSION_COOKIE_SECURE = False  # Set to True only if using HTTPS
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = 'Lax'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_DIRS = [
    BASE_DIR / 'static',
]

# Media files (not used - all images stored in MinIO)
# MEDIA_URL = '/media/'
# MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# MinIO Configuration
MINIO_ENDPOINT = f"{config('MINIO_HOST', default='localhost')}:{config('MINIO_PORT', default='9000')}"
MINIO_ACCESS_KEY = config('MINIO_ACCESS_KEY', default='minioadmin')
MINIO_SECRET_KEY = config('MINIO_SECRET_KEY', default='minioadmin123')
MINIO_BUCKET_NAME = config('MINIO_BUCKET_NAME', default='social-media-app')
MINIO_USE_HTTPS = config('MINIO_USE_HTTPS', default=False, cast=bool)

# CORS settings - allow any origin
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "http://localhost",
    "https://localhost",
    "http://127.0.0.1",
    "https://127.0.0.1",
    "http://*",
    "https://*",
]

# CSRF settings
CSRF_TRUSTED_ORIGINS = [
    'http://localhost',
    'https://localhost',
    'http://127.0.0.1',
    'https://127.0.0.1',
    'http://0.0.0.0',
    'https://0.0.0.0',
    'http://*',
    'https://*',
]

# Add dynamic CSRF origins from environment
CSRF_TRUSTED_ORIGINS.extend([
    f"http://{config('SERVER_HOST', default='localhost')}",
    f"https://{config('SERVER_HOST', default='localhost')}",
    f"http://{config('DATABASE_HOST', default='localhost')}",
    f"https://{config('DATABASE_HOST', default='localhost')}",
    f"http://{config('MINIO_HOST', default='localhost')}",
    f"https://{config('MINIO_HOST', default='localhost')}",
])

# Additional CSRF settings for Docker environment
CSRF_COOKIE_SECURE = False  # Set to True only if using HTTPS
CSRF_COOKIE_HTTPONLY = False
CSRF_USE_SESSIONS = True
CSRF_COOKIE_SAMESITE = 'Lax'

# Login/Logout URLs
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/dashboard/'
LOGOUT_REDIRECT_URL = '/login/' 