
from pathlib import Path
import os
from dotenv import load_dotenv
from django.conf import settings
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv()  # Load .env variables




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-v%3yz96r4#8&@&i5ngs^je+(4-@2=8cpz_08#tr!(t3n(=2q59'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['spbproperty.pythonanywhere.com','0.0.0.0', 'localhost', '127.0.0.1']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'property',
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'storages',
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

ROOT_URLCONF = 'backend.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'backend.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# MEDIA_URL = "/media/"
# MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = 'static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'property.CustomUser'  # Adjust the app name if it's different

CORS_ORIGIN_WHITELIST = [
   
     'http://localhost:5173',
     'https://property-management-ui-seven.vercel.app',
     'https://propertysite2.netlify.app'
     
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
}



# Stripe Keys
STRIPE_SECRET_KEY = "sk_test_51OeBjFF11zjK1PObcZa5BrJzbpgIpLpW9RyRkrlHFdDdVGbOnx1FcyPzYbtbZHp94vc6dqIYbdcVDsPTy2wvnMxO00j7O8Rl4G"
STRIPE_PUBLISHABLE_KEY = "pk_test_51OeBjFF11zjK1PObRcOLVS4OiagIrRa6TnECSaI7lrMkV59jyBDEkyLpNaz63nHJKcL7JLNmhUXTYN5oNm0cAqxX00i3WBd2FG"


STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Set this to a folder inside your project




# # # For Static Files
# # AWS_STORAGE_BUCKET_NAME = 'djangoproperty-staticfiles'
# AWS_ACCESS_KEY_ID = AWS_ACCESS_KEY_ID
# AWS_SECRET_ACCESS_KEY = AWS_SECRET_ACCESS_KEY
# # AWS_S3_REGION_NAME =os.getenv('AWS_S3_REGION_NAME')  
# # AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'

# # STATICFILES_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# # STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/'

# # For Media Files
# AWS_STORAGE_BUCKET_NAME_MEDIA = 'django-property-mediafiles'  # Separate variable for media
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_S3_CUSTOM_DOMAIN_MEDIA = f'{AWS_STORAGE_BUCKET_NAME_MEDIA}.s3.amazonaws.com'
# MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN_MEDIA}/'
AWS_ACCESS_KEY_ID = 'AKIAW4UXNNFMFXGYLPQW'
AWS_SECRET_ACCESS_KEY = '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'
AWS_STORAGE_BUCKET_NAME = 'propertys3'
AWS_S3_SIGNATURE_NAME = 's3v4'
AWS_S3_REGION_NAME = 'us-east-2'
AWS_S3_FILE_OVERWRITE = False
AWS_DEFAULT_ACL =  None
AWS_S3_VERIFY = True
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
MEDIA_URL = f'https://{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/'