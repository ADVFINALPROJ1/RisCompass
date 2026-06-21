# Accounts App - API Documentation

The `accounts` app handles user authentication and registration for RisCompass using Django REST Framework and JWT tokens.

## Features

- **User Registration** with email validation
- **JWT-based Authentication** using SimpleJWT
- **Token Refresh** mechanism for token rotation
- **Current User Endpoint** to retrieve authenticated user data
- **Password Validation** with strength checks
- **Custom User Model** for extensibility

## Endpoints

### Register
**POST** `/api/auth/register/`

Create a new user account.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "password_confirm": "SecurePass123",
  "first_name": "John",
  "last_name": "Doe"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "username": "user@example.com",
    "date_joined": "2026-06-03T10:00:00Z"
  },
  "access": "eyJhbGc...",
  "refresh": "eyJhbGc..."
}
```

**Validation:**
- `email`: Must be unique
- `password`: Minimum 8 characters
- `password` and `password_confirm`: Must match
- `first_name` and `last_name`: Optional

---

### Login
**POST** `/api/auth/login/`

Authenticate user and obtain JWT tokens.

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "username": "user@example.com",
    "date_joined": "2026-06-03T10:00:00Z"
  },
  "access": "eyJhbGc...",
  "refresh": "eyJhbGc..."
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "No active account found with the given credentials"
}
```

---

### Refresh Token
**POST** `/api/auth/token/refresh/`

Obtain a new access token using a valid refresh token.

**Request Body:**
```json
{
  "refresh": "eyJhbGc..."
}
```

**Response (200 OK):**
```json
{
  "access": "eyJhbGc..."
}
```

---

### Current User
**GET** `/api/auth/me/`

Retrieve information about the currently authenticated user.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200 OK):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "John",
  "last_name": "Doe",
  "username": "user@example.com",
  "date_joined": "2026-06-03T10:00:00Z"
}
```

**Error Response (401 Unauthorized):**
```json
{
  "detail": "Authentication credentials were not provided."
}
```

---

## JWT Token Structure

### Access Token
- **Lifetime**: 1 hour (configurable in settings)
- **Used for**: Authenticating API requests
- **Header format**: `Authorization: Bearer <access_token>`

### Refresh Token
- **Lifetime**: 7 days (configurable in settings)
- **Used for**: Obtaining new access tokens without re-logging in
- **Rotation**: Enabled (old refresh tokens are blacklisted after use)

## Authentication

All protected endpoints require a valid JWT access token in the `Authorization` header:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

### Token Refresh Flow

1. Frontend stores `access` and `refresh` tokens from login/register
2. Use `access` token for API requests
3. When access token expires (401 response), use `refresh` token to get a new access token
4. Continue with new access token
5. When refresh token expires, user must log in again

## User Serialization

### UserSerializer
Used for returning user data without exposing passwords.

**Fields:**
- `id`: User ID (read-only)
- `email`: User email
- `first_name`: First name (optional)
- `last_name`: Last name (optional)
- `username`: Username (derived from email)
- `date_joined`: Account creation date (read-only)

### RegisterSerializer
Used for user registration with password validation.

**Fields:**
- `email`: User email (unique)
- `password`: Account password (write-only, minimum 8 characters)
- `password_confirm`: Password confirmation (write-only)
- `first_name`: First name (optional)
- `last_name`: Last name (optional)

## Models

### CustomUser
Extends Django's `AbstractUser` model with:
- Unique email field
- All standard user fields (username, password, etc.)

Can be extended with domain-specific fields in the future (e.g., organization, role, preferences).

## Configuration

JWT settings are configured in `settings.py`:

```python
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
}

AUTH_USER_MODEL = 'accounts.CustomUser'
```

## Common Error Responses

### 400 Bad Request
Missing or invalid fields:
```json
{
  "email": ["This field may not be blank."],
  "password": ["Passwords do not match."]
}
```

### 401 Unauthorized
Invalid or expired token:
```json
{
  "detail": "Authentication credentials were not provided."
}
```

### 404 Not Found
User not found:
```json
{
  "detail": "Not found."
}
```

## Usage Example

### Frontend Integration (JavaScript/React)

```javascript
// 1. Register
const registerResponse = await fetch('http://localhost:8000/api/auth/register/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123',
    password_confirm: 'SecurePass123',
    first_name: 'John',
    last_name: 'Doe'
  })
});
const { access, refresh, user } = await registerResponse.json();

// 2. Store tokens
localStorage.setItem('access_token', access);
localStorage.setItem('refresh_token', refresh);

// 3. Use token for API requests
const meResponse = await fetch('http://localhost:8000/api/auth/me/', {
  headers: { 'Authorization': `Bearer ${access}` }
});
const currentUser = await meResponse.json();

// 4. Refresh token when expired
const refreshResponse = await fetch('http://localhost:8000/api/auth/token/refresh/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ refresh })
});
const { access: newAccess } = await refreshResponse.json();
localStorage.setItem('access_token', newAccess);
```

## Next Steps

- Add user profile endpoints for updating user information
- Implement password reset functionality
- Add email verification for new accounts
- Implement role-based access control (RBAC)
- Add API rate limiting
- Implement refresh token revocation (logout)
