# Django Accounts App - Setup Guide

This guide walks you through setting up and testing the RisCompass accounts app with JWT authentication.

## Quick Setup

### 1. Install Dependencies

All required packages are in `requirements.txt`. If you haven't installed them yet:

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

The accounts app uses a custom user model, so you must create migrations:

```bash
# Create migrations for the accounts app
python manage.py makemigrations accounts

# Apply all migrations
python manage.py migrate
```

If you get errors about existing auth tables, you may need to start with a fresh database:

```bash
# Option 1: Fresh start (deletes all data)
rm db.sqlite3
python manage.py migrate

# Option 2: Create superuser after migrations
python manage.py createsuperuser
```

### 3. Start the Development Server

```bash
python manage.py runserver
```

Server will be available at `http://localhost:8000`

## Testing the Accounts API

### Using cURL

#### Register a New User

```bash
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPassword123",
    "password_confirm": "TestPassword123",
    "first_name": "Test",
    "last_name": "User"
  }'
```

Expected response:
```json
{
  "user": {
    "id": 1,
    "email": "testuser@example.com",
    "first_name": "Test",
    "last_name": "User",
    "username": "testuser@example.com",
    "date_joined": "2026-06-03T10:00:00Z"
  },
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

#### Login

```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "testuser@example.com",
    "password": "TestPassword123"
  }'
```

#### Get Current User

```bash
# Replace <ACCESS_TOKEN> with the token from login/register
curl -X GET http://localhost:8000/api/auth/me/ \
  -H "Authorization: Bearer <ACCESS_TOKEN>"
```

#### Refresh Token

```bash
curl -X POST http://localhost:8000/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "<REFRESH_TOKEN>"
  }'
```

### Using Postman

1. **Import Collection** (optional)
   - Use the endpoints below in Postman

2. **Register Endpoint**
   - Method: `POST`
   - URL: `http://localhost:8000/api/auth/register/`
   - Body (raw JSON):
     ```json
     {
       "email": "postman@example.com",
       "password": "PostmanPass123",
       "password_confirm": "PostmanPass123",
       "first_name": "Postman",
       "last_name": "User"
     }
     ```

3. **Login Endpoint**
   - Method: `POST`
   - URL: `http://localhost:8000/api/auth/login/`
   - Body (raw JSON):
     ```json
     {
       "email": "postman@example.com",
       "password": "PostmanPass123"
     }
     ```
   - Save the `access` token from response

4. **Current User Endpoint**
   - Method: `GET`
   - URL: `http://localhost:8000/api/auth/me/`
   - Headers:
     - Key: `Authorization`
     - Value: `Bearer <paste_access_token_here>`

5. **Refresh Token Endpoint**
   - Method: `POST`
   - URL: `http://localhost:8000/api/auth/token/refresh/`
   - Body (raw JSON):
     ```json
     {
       "refresh": "<paste_refresh_token_here>"
     }
     ```

### Using Python

```python
import requests

BASE_URL = 'http://localhost:8000/api/auth'

# Register
register_response = requests.post(
    f'{BASE_URL}/register/',
    json={
        'email': 'python@example.com',
        'password': 'PythonPass123',
        'password_confirm': 'PythonPass123',
        'first_name': 'Python',
        'last_name': 'User'
    }
)
data = register_response.json()
access_token = data['access']
refresh_token = data['refresh']

# Get current user
me_response = requests.get(
    f'{BASE_URL}/me/',
    headers={'Authorization': f'Bearer {access_token}'}
)
print(me_response.json())

# Refresh token
refresh_response = requests.post(
    f'{BASE_URL}/token/refresh/',
    json={'refresh': refresh_token}
)
new_access_token = refresh_response.json()['access']
```

## Troubleshooting

### Migration Errors

**Error**: `django.core.exceptions.ImproperlyConfigured: AUTH_USER_MODEL refers to model 'accounts.CustomUser' that has not been installed`

**Solution**: Make sure `'apps.accounts'` is in `INSTALLED_APPS` in `settings.py` (it should be).

### "No module named 'apps'" Error

**Solution**: Make sure you're running commands from the `backend` directory:
```bash
cd backend
python manage.py migrate
```

### Email already exists error on registration

**Solution**: Use a different email address. Each email must be unique in the database.

### Token expired errors

**Solution**: This is normal. Use the `refresh` endpoint with your refresh token to get a new access token. The frontend (React) should handle this automatically with the axios interceptor.

### CORS errors when testing from frontend

**Solution**: Make sure `http://localhost:5173` (Vite dev server) is in `CORS_ALLOWED_ORIGINS` in `settings.py`.

## Integration with Frontend

The frontend (React) app is configured to use these endpoints. Make sure:

1. Frontend `.env` has correct `VITE_API_BASE_URL`:
   ```env
   VITE_API_BASE_URL=http://localhost:8000/api
   ```

2. Backend `.env` has correct `CORS_ALLOWED_ORIGINS`:
   ```env
   CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
   ```

3. Both backend and frontend are running:
   ```bash
   # Terminal 1: Backend
   cd backend
   python manage.py runserver

   # Terminal 2: Frontend
   cd frontend
   npm run dev
   ```

The frontend will automatically:
- Store tokens in localStorage
- Refresh tokens when they expire
- Add authentication headers to API requests
- Redirect to login on 401 errors

## File Structure

```
backend/apps/accounts/
├── __init__.py
├── admin.py
├── apps.py
├── models.py           # CustomUser model
├── serializers.py      # UserSerializer, RegisterSerializer
├── views.py            # API views for auth endpoints
├── urls.py             # URL routing for auth endpoints
├── tests.py
└── README.md          # API documentation
```

## Models

### CustomUser
- Extends Django's `AbstractUser`
- Unique email field
- Can be extended with additional fields (profile, preferences, etc.)

## Environment Variables

Configure these in `.env`:

```env
# Database
DB_ENGINE=django.db.backends.sqlite3
DB_NAME=db.sqlite3

# Security (generate with: python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())")
SECRET_KEY=your-secret-key-here
DEBUG=True

# JWT tokens
JWT_SECRET_KEY=your-jwt-secret-key-here
JWT_ALGORITHM=HS256

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Admin
ALLOWED_HOSTS=localhost,127.0.0.1
```

## Next Steps

1. **Test all endpoints** using the cURL/Postman examples above
2. **Verify frontend integration** by running the React app
3. **Create additional endpoints** as needed (risks, reports, etc.)
4. **Add email verification** for new registrations
5. **Implement password reset** functionality
6. **Add user profiles** with additional fields

## Resources

- [JWT Authentication with SimpleJWT](https://django-rest-framework-simplejwt.readthedocs.io/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Django Custom User Model](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model)

For more details on API endpoints, see [apps/accounts/README.md](README.md).
