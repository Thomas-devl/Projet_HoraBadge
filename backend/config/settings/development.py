"""
Development settings for HoraBadge project.
"""

from .base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-dev-key-change-in-production'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# CORS settings for development
CORS_ALLOWED_ORIGINS = [
    'http://localhost:5173',  # Vite dev server
    'http://localhost:3000',  # Alternative port
    'http://127.0.0.1:5173',
    'http://127.0.0.1:3000',
]

# Allow all origins in development (less secure, only for dev)
CORS_ALLOW_ALL_ORIGINS = True

# Additional development settings
INSTALLED_APPS += [
    'django_extensions',  # Useful dev tools
]

# Development-specific REST Framework settings
REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = [
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',  # Enable browsable API in dev
]

# Email backend for development (prints emails to console)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
