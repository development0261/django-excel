"""
Django settings for project project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

from pathlib import Path

import os.path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-=w$9qml=n^3xuhj#u62^$rfw)n0yevb7-vr*vn@t_hg6!tp9-('

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

INTERNAL_IPS = [
    # ...
    "127.0.0.1",
    # ...
]
ALLOWED_HOSTS = ['*']

AUTH_USER_MODEL = 'app.UserCustom'
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8002']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'app',
    'multiselectfield',
    'ckeditor',
    'import_export',
    'storages',







    'debug_toolbar',    
 
]
# TIME_ZONE = 'Asia/Singapore'
# USE_I18N = True
# USE_L10N = True
# USE_TZ = True

# CKEDITOR_CONFIGS = {
#     "default": {
#         "removePlugins": "stylesheetparser",
#     }
# }

# CKEDITOR_UPLOAD_PATH = ""
# CKEDITOR_FILENAME_GENERATOR = 'utils.get_filename'
# CKEDITOR_ALLOW_NONIMAGE_FILES = False

REST_FRAMEWORK = {
    'DEFAULT_PARSER_CLASSES': (
        'rest_framework_xml.parsers.XMLParser',
    ),
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework_xml.renderers.XMLRenderer',
    ),
}

MIDDLEWARE = [
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases



STATIC_URL = '/static/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'HOST': 'shaktiblog-django-database.cqocxpwhlloo.us-east-2.rds.amazonaws.com',
    'NAME': 'shaktiblog',
    'USER': 'postgres',
    'PASSWORD': 'vEuV2p!Su6=Wwxm&',
   }
}

# Django debug
# def show_toolbar(request):
#     return True
# SHOW_TOOLBAR_CALLBACK = show_toolbar

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db1.sqlite3',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = '/static/' 
STATICFILES_DIRS = [
    os.path.join(BASE_DIR,'static')
]

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media').replace('\\', '/')

MEDIA_URL = '/media/'

DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = "AKIAW5A7V7JNSMXIQINX"
AWS_SECRET_ACCESS_KEY = "vGW+cNbHvvGfmz0i2MtKEApKWYQbJ+qVi3Df7zHk"
AWS_STORAGE_BUCKET_NAME = "shaktidjangoblog-prod"
AWS_QUERYSTRING_AUTH = False

# import os
# import boto3
# from boto3.s3.transfer import S3Transfer

# local_directory = 'http://localhost:8000/'
# transfer = S3Transfer(boto3.client('s3', 'us-east-2', 
#                                    aws_access_key_id = 'AKIAW5A7V7JNSMXIQINX',
#                                    aws_secret_access_key='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'))
# client = boto3.client('s3')
# bucket = 'shaktidjangoblog-prod'
# for root, dirs, files in os.walk(local_directory):
#     for filename in files:
#         local_path = os.path.join(root, filename)
#         relative_path = os.path.relpath(local_path, local_directory)
#         s3_path = os.path.join('your s3 path',relative_path)
#         if filename.endswith('.pdf'):
#             transfer.upload_file(local_path, bucket, s3_path,extra_args={'ACL': 'public-read'})
#         else:
#             transfer.upload_file(local_path, bucket, s3_path)

# USE_S3 = 'TRUE'

# if USE_S3:
#     # aws settings
#     AWS_ACCESS_KEY_ID = "AKIAW5A7V7JNSMXIQINX"
#     AWS_SECRET_ACCESS_KEY = "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"
#     AWS_STORAGE_BUCKET_NAME = "shaktidjangoblog-prod"
#     AWS_DEFAULT_ACL = None
#     AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
#     AWS_S3_OBJECT_PARAMETERS = {'CacheControl': 'max-age=86400'}
#     # s3 static settings
#     STATIC_LOCATION = 'static'
#     STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'
#     STATICFILES_STORAGE = 'hello_django.storage_backends.StaticStorage'
#     # s3 public media settings
#     PUBLIC_MEDIA_LOCATION = 'media'
#     MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
#     DEFAULT_FILE_STORAGE = 'hello_django.storage_backends.PublicMediaStorage'
# else:
#     STATIC_URL = '/staticfiles/'
#     STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
#     MEDIA_URL = '/media/images/'
#     MEDIA_ROOT = os.path.join(BASE_DIR, 'media/images')

# STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)

