# Project Name

Full-stack web application with Django REST Framework backend and Vue.js frontend.

## Project Structure

```
project/
├── backend/              # Django REST API
├── frontend/             # Vue.js SPA
├── docker/              # Docker configuration
└── docs/                # Documentation
```

## Tech Stack

### Backend
- Python 3.12+
- Django 4.2+
- Django REST Framework
- PostgreSQL (production) / SQLite (development)

### Frontend
- Vue.js 3
- Vite
- Vue Router
- Pinia (state management)
- Axios

## Getting Started

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL (for production)
- Docker & Docker Compose (optional)

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy environment file:
```bash
cp .env.example .env
```

5. Run migrations:
```bash
python manage.py migrate
```

6. Create superuser:
```bash
python manage.py createsuperuser
```

7. Run development server:
```bash
python manage.py runserver
```

API will be available at: `http://localhost:8000`

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Copy environment file:
```bash
cp .env.example .env
```

4. Run development server:
```bash
npm run dev
```

App will be available at: `http://localhost:5173`

### Docker Setup

1. Copy environment files:
```bash
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

2. Build and run with Docker Compose:
```bash
docker-compose up --build
```

- Backend API: `http://localhost:8000`
- Frontend: `http://localhost:3000`
- Admin panel: `http://localhost:8000/admin`

## Development

### Backend Commands

```bash
# Run tests
python manage.py test

# Create new app
python manage.py startapp app_name apps/app_name

# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic
```

### Frontend Commands

```bash
# Run dev server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Project Configuration

### Django Settings
- `base.py` - Common settings
- `development.py` - Development environment
- `production.py` - Production environment

Set environment with: `export DJANGO_ENV=development` or `export DJANGO_ENV=production`

### API Documentation
API documentation available at:
- Swagger UI: `http://localhost:8000/api/docs/`
- ReDoc: `http://localhost:8000/api/redoc/`

## Deployment

### Production Checklist
- [ ] Update `SECRET_KEY` in production
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Setup PostgreSQL database
- [ ] Configure static files serving
- [ ] Setup HTTPS/SSL
- [ ] Configure CORS settings
- [ ] Setup monitoring and logging

## Contributing

1. Create a feature branch
2. Make your changes
3. Write/update tests
4. Submit a pull request

## License

[Your License Here]
