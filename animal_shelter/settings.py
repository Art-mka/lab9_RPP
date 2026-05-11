import os
import dj_database_url
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# Безопасность
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-e$r%#g@sj3v$f9+rvcju2w81!jn*g@h+kzind(qf8=6re_dua*')
DEBUG = os.environ.get('DEBUG', 'False') == 'True'

# Определяем ALLOWED_HOSTS для Render
if os.environ.get('RENDER'):
    ALLOWED_HOSTS = [os.environ.get('RENDER_EXTERNAL_HOSTNAME', ''),
                     'localhost', '127.0.0.1']
    ALLOWED_HOSTS = [host for host in ALLOWED_HOSTS if host]
else:
    ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# CSRF доверенные источники
CSRF_TRUSTED_ORIGINS = [f'https://{host}' for host in ALLOWED_HOSTS if host]

# Приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'animals',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'animal_shelter.urls'

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

WSGI_APPLICATION = 'animal_shelter.wsgi.application'

# База данных
if os.environ.get('DATABASE_URL'):
    DATABASES = {
        'default': dj_database_url.config(
            conn_max_age=600,
            conn_health_checks=True,
        )
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Проверка паролей
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Интернационализация
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Europe/Moscow'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Настройки авторизации
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = 'login'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'