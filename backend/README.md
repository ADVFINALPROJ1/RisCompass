# RisCompass Backend 🧭⚙️

This is the Django REST Framework backend service for RisCompass, providing JWT authentication, business snapshot storage, risk assessment scoring engines, World Bank data caching, and an AI interview session generator utilizing the Google Gemini API.

---

## 🏗️ Backend Architecture & Project Structure

The backend utilizes modular Django applications, each containing its own models, serializers, views, and urls, isolated under `apps/`:

```text
backend/
├── apps/
│   ├── accounts/         # Custom User model and JWT registration/login
│   ├── regions/          # Supported countries/cities with data availability settings
│   ├── industries/       # Industry definitions and customizable risk weights
│   ├── snapshots/        # User-created business snapshot profiles
│   ├── external_data/    # World Bank API caching layer and indicators
│   ├── risks/            # Scoring engine calculations and risk report storage
│   ├── interviews/       # AI question generating logic and user answer processing
│   └── comparisons/      # Side-by-side snapshot comparison models
├── config/               # Django project settings (settings.py, urls.py, wsgi.py)
├── manage.py             # Django entrypoint script
├── requirements.txt      # Python package dependencies
└── .env                  # Local configuration secrets
```

---

## 🛠️ Installation & Setup

### 1. Prerequisites
* Python 3.11+
* PostgreSQL (Optional: SQLite is used as the default fallback database)

### 2. Virtual Environment Creation
```bash
# Navigate to the backend directory
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Database Migrations
Run migrations to build database tables:
```bash
python manage.py migrate
```

### 5. Seeding Seed Data
To populate the database with baseline regions, industries, weights, and interview questions, run the following commands:
```bash
# Seed initial regions (Berlin, London, Remote Ethiopia) and industries with weights
python manage.py seed_initial_data

# Seed baseline AI-assisted interview questions
python manage.py seed_interview_questions
```

### 6. Create Admin User
```bash
python manage.py createsuperuser
```

### 7. Run Server
```bash
python manage.py runserver
```
The API server will run at `http://localhost:8000/`.

---

## 🔑 Environment Variables (`.env`)

Configure these values in your local `.env` file in the root of the `backend/` directory:

```env
SECRET_KEY=django-insecure-your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Optional PostgreSQL setup (default is SQLite)
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=riscompass_db
# DB_USER=postgres
# DB_PASSWORD=your_password
# DB_HOST=localhost
# DB_PORT=5432

# External Integrations
GEMINI_API_KEY=your_google_gemini_api_key
WORLD_BANK_API_BASE_URL=https://api.worldbank.org/v2
```

---

## 🔌 API Endpoints Reference

### 🔐 Authentication (`/api/auth/`)
* `POST /auth/register/` - Create a new user account.
* `POST /auth/login/` - Login and get JWT access + refresh tokens.
* `POST /auth/token/refresh/` - Refresh expired access token.
* `GET /auth/me/` - Retrieve authenticated user profile (Requires Header: `Authorization: Bearer <JWT>`).

### 📦 Snapshots & Reports (`/api/`)
* `GET /api/snapshots/` - List user snapshots.
* `POST /api/snapshots/` - Create a new business profile.
* `GET /api/snapshots/<id>/` - Retrieve snapshot details.
* `POST /api/snapshots/<id>/report/` - Generate a risk report (automatically determines if World Bank query or AI interview is required).
* `GET /api/reports/<id>/` - View generated risk report breakdown.

### 💬 Interactive Interview Flow (`/api/interviews/`)
* `POST /api/interviews/sessions/` - Start an interview session for low-data regions.
* `GET /api/interviews/sessions/<id>/` - Fetch interview questions.
* `POST /api/interviews/sessions/<id>/answers/` - Submit answers and trigger AI insight scoring.

### 📊 Comparisons (`/api/comparisons/`)
* `POST /api/comparisons/` - Create and retrieve side-by-side snapshot risk analysis comparisons.

---

## 🧪 Testing the API

To verify that registration and login are running correctly, execute these curl commands:

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123","password_confirm":"SecurePass123","first_name":"Jane","last_name":"Doe"}'

# Login
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"SecurePass123"}'
```
