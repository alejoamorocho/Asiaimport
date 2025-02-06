# Installation Guide

## Prerequisites

- Docker and Docker Compose
- Git
- Node.js 18+ (for local development)
- Python 3.12+ (for local development)

## Quick Start with Docker

1. Clone the repository:
```bash
git clone https://github.com/your-username/cosmedical-import.git
cd cosmedical-import
```

2. Create a `.env` file in the root directory:
```env
DEBUG=1
SECRET_KEY=your-secret-key-here
COMPANY_NAME=Your Company Name
SEND_PDF_NOTIFICATIONS=1

# Database
POSTGRES_DB=cosmedical_db
POSTGRES_USER=cosmedical_user
POSTGRES_PASSWORD=your-secure-password

# Redis
REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
```

3. Build and start the containers:
```bash
docker-compose up --build
```

4. Create a superuser:
```bash
docker-compose exec backend python manage.py createsuperuser
```

The application will be available at:
- Frontend: http://localhost:5173
- Backend API: http://localhost:8000
- Admin Interface: http://localhost:8000/admin

## Manual Installation (Development)

### Backend Setup

1. Create a virtual environment:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install system dependencies for WeasyPrint:
```bash
# Ubuntu/Debian
sudo apt-get install build-essential python3-dev python3-pip python3-setuptools python3-wheel python3-cffi libcairo2 libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0 libffi-dev shared-mime-info

# Windows
# Install GTK3 runtime from https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer
```

4. Set up the database:
```bash
python manage.py migrate
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

6. Start Celery worker:
```bash
celery -A core worker -l INFO
```

### Frontend Setup

1. Install dependencies:
```bash
cd frontend
npm install
```

2. Start development server:
```bash
npm run dev
```

## Running Tests

### Backend Tests
```bash
cd backend
python manage.py test
```

With coverage:
```bash
coverage run manage.py test
coverage report
```

### Frontend Tests
```bash
cd frontend
npm test
```

## Deployment

### Production Considerations

1. Update environment variables:
   - Set `DEBUG=0`
   - Use a strong `SECRET_KEY`
   - Configure proper database credentials
   - Set up email settings for notifications

2. Configure SSL/TLS:
   - Obtain SSL certificate
   - Configure Nginx as reverse proxy

3. Set up monitoring:
   - Configure logging
   - Set up error tracking (e.g., Sentry)
   - Monitor system resources

4. Database backups:
   - Configure automated backups
   - Test backup restoration

### Production Deployment Steps

1. Build production images:
```bash
docker-compose -f docker-compose.prod.yml build
```

2. Start services:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

3. Apply migrations:
```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py migrate
```

4. Collect static files:
```bash
docker-compose -f docker-compose.prod.yml exec backend python manage.py collectstatic
```

## Troubleshooting

### Common Issues

1. PDF Generation Issues:
   - Verify WeasyPrint dependencies are installed
   - Check file permissions in media directory
   - Verify Redis connection for Celery

2. Database Connection Issues:
   - Verify PostgreSQL is running
   - Check database credentials
   - Ensure database migrations are applied

3. Frontend Build Issues:
   - Clear node_modules and reinstall
   - Verify Node.js version
   - Check for conflicting dependencies

### Getting Help

- Check the issue tracker on GitHub
- Review the logs: `docker-compose logs -f [service_name]`
- Contact support team
