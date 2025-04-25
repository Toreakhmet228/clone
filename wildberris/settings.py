import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

# Загрузка переменных окружения из .env
load_dotenv()

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ (рекомендуется хранить в .env для продакшена)
SECRET_KEY = os.getenv('SECRET_KEY', 'django-insecure-#3_p!12^*w$xnvel2pn7*t7ciyme3!$m7rhsrvzts$k(a@fia4')

# Режим отладки (отключите в продакшене)
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Разрешенные хосты
ALLOWED_HOSTS = ['localhost', '127.0.0.1', 'freelance.com.kz', 'www.freelance.com.kz']

# Установленные приложения
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'shtoto_app',  # Ваше приложение
    'rest_framework',
    'rest_framework_simplejwt',  # Для JWT-аутентификации
    'corsheaders',  # Для обработки CORS
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',  # CORS должен быть перед CommonMiddleware
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Конфигурация REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

# Настройки Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),  # Время жизни access_token
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),     # Время жизни refresh_token
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': os.getenv('SECRET_KEY', 'django-insecure-#3_p!12^*w$xnvel2pn7*t7ciyme3!$m7rhsrvzts$k(a@fia4'),
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',
    'JTI_CLAIM': 'jti',
}

# CORS настройки
CORS_ALLOWED_ORIGINS = [
    'http://localhost:4200',  # Angular dev server
]

CSRF_TRUSTED_ORIGINS = [
    'http://localhost:4200',  # Для CSRF-запросов от Angular
]

# Настройки Stripe (рекомендуется хранить в .env)
STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', 'sk_test_51RCQhIDCxoz1BPr0SGP0FS7XydDYPCG7sk1FcQgf0CyTr0yDeuT7qBsdfhaRQ6xXGSOh4yxJbQ7qdDZygPEdL7C800gZZLItkQ')
STRIPE_PUBLISHABLE_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY', 'pk_test_51RCQhIDCxoz1BPr00RZx3ts90Q6s0cyU3MicDWfaMY8LAD8N1BEXh3lyI92pv97t5KGLKGy4nCcnItLSUfnLHMz200eUPlY3If')
STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '#m__4[unmRtXD4_RG[wHXk}[X-c9Q&QJ')
DOMAIN = os.getenv('DOMAIN', 'http://localhost:4200')

# Настройки YooKassa (если используются)
YOOKASSA_SHOP_ID = os.getenv('YOOKASSA_SHOP_ID', 'your-shop-id')
YOOKASSA_SECRET_KEY = os.getenv('YOOKASSA_SECRET_KEY', 'your-secret-key')

# URL-конфигурация
ROOT_URLCONF = 'wildberris.urls'

# Настройки шаблонов
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

# WSGI-приложение
WSGI_APPLICATION = 'wildberris.wsgi.application'

# Настройки базы данных
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Валидаторы паролей
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

# Локализация
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Статические файлы
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Медиа-файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Тип первичного ключа по умолчанию
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'