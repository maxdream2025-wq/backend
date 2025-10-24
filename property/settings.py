from pathlib import Path
import os
from urllib.parse import urlparse
import dj_database_url 

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Cloudinary Configuration
import cloudinary

cloudinary.config(
    cloud_name="dkjpnznbf",  # Your actual cloud name from dashboard
    api_key="342237737429874",  # Using the "Root" API key that matches your secret
    api_secret="Ri8sum7h-eoYmforhXYlNHZ5Bu8"  # Your actual API secret
)

# Media files configuration - now using Cloudinary
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-qgto76gprzxhcq1gg5qvsu=(05e0ftubymh$8*t49xtai9e%r3')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get('DEBUG', 'True') == 'True'

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'propertyCrud',
    'corsheaders',
    'news',
    'testimonial',
    'inquiry',
    'newsletter',
    'contact',
    'career',
    'cloudinary',
    'cloudinary_storage',
]

# Cloudinary Storage Configuration
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'dkjpnznbf',  # Your actual cloud name from dashboard
    'API_KEY': '342237737429874',  # Using the "Root" API key that matches your secret
    'API_SECRET': 'Ri8sum7h-eoYmforhXYlNHZ5Bu8',  # Your actual API secret
    'MEDIA_TAG': 'remax_media',
    'INVALID_VIDEO_ERROR_MESSAGE': 'Please upload a valid video file.',
    'STATIC_TAG': 'remax_static',
    'STATIC_IMAGES_EXTENSIONS': ['jpg', 'jpeg', 'png', 'gif', 'webp'],
    'MAGIC_FILE_PATH': 'magic',
    'STATIC_IMAGES_TRANSFORMATIONS': {
        'format': 'auto',
        'quality': 'auto',
        'fetch_format': 'auto',
    }
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'property.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'property.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'remaxdb',         # your PostgreSQL database name
        'USER': 'remaxuser',       # your PostgreSQL user
        'PASSWORD': 'Abcd.@123456', # user password
        'HOST': '72.60.211.107',       # or your VPS IP if remote
        'PORT': '5432',            # default PostgreSQL port
    }
}



# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

CORS_ALLOWED_ORIGINS = [
    "https://remaxdreamuae.com",     # your production domain (https)
    "https://www.remaxdreamuae.com", # www version
    "http://72.60.211.107:3000",    # React dev server
    "http://localhost:3000",         # local development
    "http://72.60.211.107:3001", 
]
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/

STATIC_URL = 'static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Email Configuration
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'cool.saa733@gmail.com'
EMAIL_HOST_PASSWORD = 'lssm roxh pksg zxcy'
DEFAULT_FROM_EMAIL = 'info@remaxdreamuae.com'

# Newsletter notification email
NEWSLETTER_NOTIFICATION_EMAIL = 'info@remaxdreamuae.com'

# Inquiry notification email
INQUIRY_NOTIFICATION_EMAIL = 'info@remaxdreamuae.com'

# Contact form notification email
CONTACT_NOTIFICATION_EMAIL = 'info@remaxdreamuae.com'

# Career application notification email
CAREER_NOTIFICATION_EMAIL = 'info@remaxdreamuae.com'

# CC email for all notifications - REMOVED
# CC_EMAIL = 'basatali326@gmail.com' 

# Frontend URL for email links
FRONTEND_URL = 'https://remaxdreamuae.com'

# Django REST Framework: No global pagination
REST_FRAMEWORK = {}

# Security settings for HTTPS
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SECURE_SSL_REDIRECT = False  # Set to True if you want to force HTTPS redirects
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True