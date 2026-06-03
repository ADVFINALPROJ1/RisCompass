# RisCompass Backend

Django REST Framework API for the RisCompass risk assessment application.

## Setup Instructions

### 1. Prerequisites

- Python 3.11+
- PostgreSQL (optional, SQLite used by default for development)
- Virtual environment tool (venv, virtualenv, or similar)

### 2. Create and Activate Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

Since All Members use Windows

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

1. Copy `.env.local` to `.env`:
   ```bash
   cp .env.local .env
   ```

2. Edit `.env` and update the following:
   - `SECRET_KEY`: Generate a new secure key (run `python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"`)
   - `DEBUG`: Set to `False` for production
   - `DB_PASSWORD`: our PostgreSQL password (if using PostgreSQL)
   - `GEMINI_API_KEY`: our Google Gemini API key
   - `JWT_SECRET_KEY`: Generate another secure key for JWT

### 5. Configure PostgreSQL


```bash
# Create a PostgreSQL database
createdb riscompass_db

# Update .env with PostgreSQL credentials:
DB_ENGINE=django.db.backends.postgresql
DB_NAME=riscompass_db
DB_USER=postgres
DB_PASSWORD= our shared secret password
DB_HOST=localhost
DB_PORT=5432
```

### 6. Run Migrations

```bash
python manage.py migrate
```

### 7. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

### 8. Start the Development Server

```bash
python manage.py runserver
```

The API will be available at `http://localhost:8000`.

## Project Structure

```text
backend/
├── config/              # Django configuration (urls.py, wsgi.py, asgi.py)
├── apps/                # Django applications (to be created)
│   ├── users/
│   ├── risks/
│   ├── reports/
│   └── ...
├── templates/           # HTML templates (if needed)
├── settings.py          # Django settings with environment variable support
├── manage.py            # Django management script
├── requirements.txt     # Python dependencies
├── .env.example         # Example environment file
└── README.md            # This file
```

## Creating Django Apps

To create new apps within the backend:

```bash
python manage.py startapp app_name
```

Then add `app_name` to the `INSTALLED_APPS` list in `settings.py`.

## API Endpoints

Base URL: `http://localhost:8000/api/`

### Authentication (Accounts App)
- `POST /auth/register/` — Register a new user
- `POST /auth/login/` — Login and obtain JWT tokens
- `POST /auth/token/refresh/` — Refresh an expired access token
- `GET /auth/me/` — Get current user information (requires authentication)

For detailed authentication API documentation, see [apps/accounts/README.md](apps/accounts/README.md).

### Available Endpoints (to be implemented)
- `/v1/risks/` — Risk assessment endpoints
- `/v1/reports/` — Reports endpoints
- `/v1/users/` — User management endpoints

## Admin Panel

Access the Django admin panel at `http://localhost:8000/admin/` using your superuser credentials.

## Testing the API

### Register and Login

```bash
# Register a new user
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123",
    "password_confirm": "SecurePass123",
    "first_name": "John",
    "last_name": "Doe"
  }'

# Login with credentials
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123"
  }'

# Get current user (requires valid access token)
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <access_token>"

# Refresh access token
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{"refresh": "<refresh_token>"}'
```

## Debugging

- Check logs in the terminal running the dev server
- Use Django shell for quick testing: `python manage.py shell`
- Enable `DEBUG=True` in `.env` for detailed error pages

## Common Issues

- **Port 8000 already in use**: Run on a different port with `python manage.py runserver 8001`
- **Database connection error**: Verify PostgreSQL is running and credentials in `.env` are correct
- **CORS errors**: Check `CORS_ALLOWED_ORIGINS` in `settings.py` matches your frontend URL

## Next Steps

1. Create the `apps` folder and organize Django apps
2. Implement models for Risks, Reports, and Users
3. Create serializers and viewsets for each app
4. Write unit tests
5. Set up GitHub Actions for CI/CD
