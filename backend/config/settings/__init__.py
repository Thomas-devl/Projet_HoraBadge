"""
Settings package initialization.
By default, use development settings.
Override with environment variable: DJANGO_SETTINGS_MODULE
"""

import os

# Determine which settings to use based on environment
environment = os.environ.get('DJANGO_ENV', 'development')

if environment == 'production':
    from .production import *
elif environment == 'development':
    from .development import *
else:
    from .base import *
