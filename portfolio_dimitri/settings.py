"""
Django settings for portfolio_dimitri project.
Optimized for production with security and performance best practices.
"""

import os
from pathlib import Path

import dj_database_url
import sentry_sdk  # Single import
from django.core.management.utils import get_random_secret_key
from dotenv import load_dotenv
from sentry_sdk.integrations.django import DjangoIntegration

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ==============================================================================
# CORE SETTINGS
# ==============================================================================

def _str_to_bool(value):
    """Convert string to boolean."""
    return str(value).lower() in {"1", "true", "yes", "on"}


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')
if not SECRET_KEY:
    if os.environ.get('ENVIRONMENT') == 'production':
        raise ValueError("SECRET_KEY must be set in production!")
    SECRET_KEY = get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = _str_to_bool(os.environ.get('DEBUG', 'False'))

# Environment
ENVIRONMENT = os.environ.get('ENVIRONMENT', 'development' if DEBUG else 'production')

# Google Analytics & Monitoring
GOOGLE_ANALYTICS_ID = os.environ.get('GOOGLE_ANALYTICS_ID', '')
SENTRY_DSN = os.environ.get('SENTRY_DSN', '')
SITE_URL = os.environ.get('SITE_URL', 'http://localhost:8000' if DEBUG else 'https://dim-gggl.com')

# Allowed hosts
ALLOWED_HOSTS = [
    h.strip() 
    for h in os.environ.get('ALLOWED_HOSTS', '127.0.0.1,localhost').split(',') 
    if h.strip()
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [
    origin.strip()
    for origin in os.environ.get('CSRF_TRUSTED_ORIGINS', '').split(',')
    if origin.strip()
]

# Maintenance mode
MAINTENANCE_MODE = _str_to_bool(os.environ.get('MAINTENANCE_MODE', 'False'))


# ==============================================================================
# APPLICATION DEFINITION
# ==============================================================================

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sitemaps',
    # Third-party
    'whitenoise.runserver_nostatic',
    'compressor',
    # Local apps
    'core',
    'projects',
]

# Note: django_ratelimit requires Redis. Use custom rate_limit decorator in development.

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'core.middleware.MaintenanceModeMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middleware.SecurityHeadersMiddleware',
]

# Add cache middleware in production only
if not DEBUG:
    MIDDLEWARE = [
        'django.middleware.cache.UpdateCacheMiddleware',
        *MIDDLEWARE,
        'django.middleware.cache.FetchFromCacheMiddleware',
    ]

# Add query count middleware in development only
if DEBUG:
    MIDDLEWARE.append('core.middleware.QueryCountDebugMiddleware')

ROOT_URLCONF = 'portfolio_dimitri.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.template.context_processors.media',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'core.context_processors.global_settings',
                'core.context_processors.site_info',  # NEW: Site-wide info
            ],
        },
    },
]

WSGI_APPLICATION = 'portfolio_dimitri.wsgi.application'


# ==============================================================================
# DATABASE
# ==============================================================================

_db_engine = os.environ.get('DB_ENGINE', 'django.db.backends.sqlite3')
_is_postgres = 'postgresql' in _db_engine

DATABASES = {
    'default': {
        'ENGINE': _db_engine,
        'NAME': os.environ.get('DB_NAME', str(BASE_DIR / 'db.sqlite3')),
    }
}

# Add PostgreSQL-specific settings
if _is_postgres:
    DATABASES['default'].update({
        'USER': os.environ.get('DB_USER', ''),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', '127.0.0.1'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': int(os.environ.get('CONN_MAX_AGE', '600')),
        'OPTIONS': {
            'connect_timeout': 10,
        } if not DEBUG else {},
    })

# Override with DATABASE_URL if available
_database_url = os.environ.get('DATABASE_URL')
if _database_url:
    DATABASES['default'] = dj_database_url.config(
        default=_database_url,
        conn_max_age=int(os.environ.get('CONN_MAX_AGE', '600')),
        conn_health_checks=True,
        ssl_require=not DEBUG,
    )


# ==============================================================================
# PASSWORD VALIDATION
# ==============================================================================

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


# ==============================================================================
# INTERNATIONALIZATION
# ==============================================================================

LANGUAGE_CODE = 'fr-fr'
TIME_ZONE = 'Europe/Paris'
USE_I18N = True
USE_TZ = True


# ==============================================================================
# STATIC FILES & MEDIA
# ==============================================================================

STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

# Storage configuration
STORAGES = {
    "default": {
        "BACKEND": "django.core.files.storage.FileSystemStorage",
    },
    "staticfiles": {
        "BACKEND": "django.contrib.staticfiles.storage.ManifestStaticFilesStorage,
    },
}

# Django Compressor
COMPRESS_ENABLED = not DEBUG
COMPRESS_OFFLINE = not DEBUG

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'


# ==============================================================================
# CACHING
# ==============================================================================

_redis_url = os.environ.get('REDIS_URL')
if _redis_url and not DEBUG:
    CACHES = {
        'default': {
            'BACKEND': 'django_redis.cache.RedisCache',
            'LOCATION': _redis_url,
            'OPTIONS': {
                'CLIENT_CLASS': 'django_redis.client.DefaultClient',
                'SOCKET_CONNECT_TIMEOUT': 5,
                'SOCKET_TIMEOUT': 5,
                'CONNECTION_POOL_KWARGS': {
                    'max_connections': 50,
                    'retry_on_timeout': True,
                },
                'COMPRESSOR': 'django_redis.compressors.zlib.ZlibCompressor',
            },
            'KEY_PREFIX': 'portfolio',
            'TIMEOUT': 60 * 15,
        }
    }
else:
    # Use LocMemCache in development (supports atomic operations for django-ratelimit)
    CACHES = {
        'default': {
            'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
            'LOCATION': 'portfolio-dev-cache',
            'TIMEOUT': 60 * 15,
            'OPTIONS': {
                'MAX_ENTRIES': 1000,
            },
        }
    }

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60 * 15
CACHE_MIDDLEWARE_KEY_PREFIX = 'portfolio'


# ==============================================================================
# SECURITY SETTINGS
# ==============================================================================

if not DEBUG:
    # SSL/HTTPS
    SECURE_SSL_REDIRECT = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    
    # Cookies
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    CSRF_COOKIE_SECURE = True
    CSRF_COOKIE_HTTPONLY = True
    CSRF_COOKIE_SAMESITE = 'Lax'
    
    # Security headers
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_BROWSER_XSS_FILTER = True
    X_FRAME_OPTIONS = 'DENY'
    SECURE_REFERRER_POLICY = 'strict-origin-when-cross-origin'
    
    # HSTS
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

# Content Security Policy
CONTENT_SECURITY_POLICY = " ".join([
    "default-src 'self'",
    "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://www.googletagmanager.com",
    "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com",
    "font-src 'self' https://fonts.gstatic.com",
    "img-src 'self' data: https:",
    "connect-src 'self' https://www.google-analytics.com https://www.googletagmanager.com",
    "frame-ancestors 'none'",
    "base-uri 'self'",
    "form-action 'self'",
])


# ==============================================================================
# LOGGING
# ==============================================================================

LOG_DIR = BASE_DIR / 'logs'
if DEBUG:
    os.makedirs(LOG_DIR, exist_ok=True)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[{levelname}] {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '[{levelname}] {message}',
            'style': '{',
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
        'file': {
            'level': 'WARNING',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': str(LOG_DIR / 'portfolio.log'),
            'maxBytes': 10 * 1024 * 1024,  # 10 MB
            'backupCount': 5,
            'formatter': 'verbose',
            'filters': ['require_debug_true'],
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler',
            'filters': ['require_debug_false'],
            'include_html': True,
        },
    },
    'root': {
        'handlers': ['console'] + (['file'] if DEBUG else []),
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'] + (['file'] if DEBUG else []),
            'level': 'INFO',
            'propagate': False,
        },
        'django.request': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console', 'mail_admins'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.db.backends': {
            'handlers': ['console'],
            'level': 'DEBUG' if DEBUG else 'INFO',
            'propagate': False,
        },
        'portfolio': {
            'handlers': ['console'] + (['file'] if DEBUG else []),
            'level': 'INFO',
            'propagate': False,
        },
    },
}


# ==============================================================================
# SENTRY MONITORING
# ==============================================================================

if SENTRY_DSN:
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(
                transaction_style='url',
                middleware_spans=True,
                signals_spans=True,
                cache_spans=True,
            ),
        ],
        environment=ENVIRONMENT,
        traces_sample_rate=float(os.environ.get('SENTRY_TRACES_SAMPLE_RATE', '0.1')),
        profiles_sample_rate=float(os.environ.get('SENTRY_PROFILES_SAMPLE_RATE', '0.1')),
        send_default_pii=False,
        attach_stacktrace=True,
        enable_tracing=True,
        ignore_errors=[
            'django.http.response.Http404',
            'django.core.exceptions.PermissionDenied',
        ],
        _experiments={
            "profiles_sample_rate": float(os.environ.get('SENTRY_PROFILES_SAMPLE_RATE', '0.1')),
        },
    )


# ==============================================================================
# PORTFOLIO SPECIFIC SETTINGS
# ==============================================================================

# Personal information (centralized instead of hardcoded in views)
PORTFOLIO_PERSON = {
    'name': 'Dimitri Gaggioli',
    'title': 'Python Developer - Backend',
    'baseline': 'Think. Code. Push.',
    'location': 'Paris',
    'contact_email': 'dimitri.gaggioli@gmail.com',
    'contact_phone': '+33620156172',
    'github': 'https://github.com/dim-gggl',
    'linkedin': 'https://www.linkedin.com/in/dimitri-gaggioli/',
    'years_experience': 14,
}

# Project list constants
PROJECTS_PER_PAGE = 4
FEATURED_PROJECTS_COUNT = 2
SIMILAR_PROJECTS_COUNT = 2


# ==============================================================================
# MISCELLANEOUS
# ==============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Admin site customization
ADMIN_SITE_HEADER = "Portfolio Dimitri - Administration"
ADMIN_SITE_TITLE = "Portfolio Admin"
ADMIN_INDEX_TITLE = "Bienvenue dans l'administration"