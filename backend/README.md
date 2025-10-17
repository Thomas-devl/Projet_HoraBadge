# Backend Documentation

## Structure

- `config/` - Django project configuration
  - `settings/` - Modular settings (base, development, production)
  - `urls.py` - Main URL configuration
  - `wsgi.py` - WSGI configuration
  - `asgi.py` - ASGI configuration
- `apps/` - Django applications
- `static/` - Static files
- `media/` - User-uploaded files
- `tests/` - Project-wide tests
- `scripts/` - Utility scripts

## Creating a New App

```bash
python manage.py startapp app_name apps/app_name
```

Then add `'apps.app_name'` to `INSTALLED_APPS` in `config/settings/base.py`

## Best Practices

1. Use Django REST Framework for APIs
2. Keep apps small and focused
3. Write tests for all functionality
4. Use serializers for data validation
5. Follow Django coding style
6. Use environment variables for secrets
