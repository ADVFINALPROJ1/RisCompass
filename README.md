# RisCompass

RisCompass is a student-built full-stack risk assessment application for school projects. It helps users compare business risk across regions, industries, and economic indicators by combining a Django REST API backend with a React Vite frontend.

## Key Features

- Risk scoring and comparative analysis for regions and industries
- Economic data integration via the World Bank API
- AI-assisted guidance using the Gemini API
- Interactive charts and dashboards built with Recharts
- User-friendly reports and comparison views

## Tech Stack

- Backend: Django REST Framework, PostgreSQL, Python
- Frontend: React, Vite, Tailwind CSS
- External APIs: World Bank API, Gemini API
- Charts: Recharts
- API Test: Postman

## Getting Started

### Prerequisites

- Python 3.11+ (or compatible)
- PostgreSQL
- Node.js 24.16.0 The LTS Version(Stable) and npm 11.13.0

### Local Development

1. Clone the repository:
   ```bash
   git clone https://github.com/ADVFINALPROJ1/RisCompass.git
   cd RisCompass
   ```
2. Set up the backend environment:
   - Create a Python virtual environment
   - Install backend dependencies
   - Configure PostgreSQL connection settings in a `.env` or Django settings module
3. Set up the frontend environment:
   - Install frontend dependencies
   - Configure any required API keys in `.env.local`
4. Run backend and frontend services locally.

## Project Structure

```text
RisCompass/
├── backend/           # Django REST API and backend services
├── frontend/          # React Vite application
├── docs/              # Project documentation and design notes
├── .github/           # GitHub workflows and templates
├── .gitignore         # Files and folders to ignore in Git
└── README.md          # Project overview and setup guide
```

## Contribution

Pull request template in `.github/PULL_REQUEST_TEMPLATE.md` and keep commit messages clear.

## Notes

- Keep secrets and API keys out of the repository
- Use `.env` files for local configuration
- Document any architectural decisions in `docs/`
