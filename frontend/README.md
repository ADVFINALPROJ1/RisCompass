# RisCompass Frontend 🧭💻

This is the React + Vite + Tailwind CSS frontend application for RisCompass. It offers a premium, modern dashboard UI featuring custom visualization charts (Recharts), reactive multi-step forms, a comparison tool, and an interactive step-by-step interview wizard.

---

## 🎨 Design System & UI Principles
RisCompass frontend utilizes **Vanilla CSS** coupled with **Tailwind CSS** configuration to create a premium visual experience:
* **Glassmorphism**: Elegant card borders, subtle background blurs, and premium dark/light toggles.
* **Modern Typography**: Inter and Outfit Google Fonts for high readability.
* **Micro-Animations**: Hover-triggered translations, fading transition entries, and shimmer effect indicators.
* **Color Palettes**: Harmony of slate-gray neutrals combined with energetic primary blue (`#3b82f6`) and green (`#10b981`) gradients.

---

## 🗂️ Project Structure

The project structure keeps components, contexts, pages, styles, and api wrappers decoupled:

```text
frontend/
├── src/
│   ├── api/                  # API client modules
│   │   ├── accountsApi.js    # Register, login, and profile fetching
│   │   ├── snapshotsApi.js   # Creation and listing of snapshots
│   │   ├── reportsApi.js     # Generating and reading risk reports
│   │   ├── regionsApi.js     # Loading geographic options
│   │   └── industriesApi.js  # Loading industry classes
│   ├── components/           # Reusable UI widgets
│   │   ├── Navbar.jsx        # Navigation header
│   │   ├── ProtectedRoute.jsx# Auth route guard
│   │   ├── ConfidenceGauge.jsx# SVG score gauge
│   │   ├── RiskRadarChart.jsx # Recharts radar breakdown
│   │   ├── RiskFactorList.jsx # Listing of individual risk items
│   │   └── LoadingSpinner.jsx # Visual loading feedback
│   ├── context/              # Context State Providers
│   │   └── AuthContext.jsx   # Global user login state management
│   ├── pages/                # High-level page views
│   │   ├── Login.jsx         # Login form page
│   │   ├── Register.jsx      # Registration form page
│   │   ├── Dashboard.jsx     # User command center and snapshot lists
│   │   ├── CreateSnapshot.jsx# Multi-step business setup wizard
│   │   ├── SnapshotDetail.jsx# Detailed snapshot overview
│   │   ├── InterviewPage.jsx # AI interactive questionnaire
│   │   ├── ReportPage.jsx    # Visualized risk reports
│   │   └── ComparePage.jsx   # Side-by-side snapshot compare utility
│   ├── styles/               # CSS assets
│   │   └── index.css         # Custom stylesheet and Tailwind base
│   └── utils/
│       └── api.js            # Axios client with JWT auto-inject & token refresh interceptors
├── package.json              # Core package configurations
└── tailwind.config.js        # Design tokens and tailwind utilities
```

---

## 🚀 Installation & Running

### 1. Prerequisites
* Node.js (v18+ recommended)
* npm (v9+ recommended)

### 2. Install Package Dependencies
```bash
# Navigate to the frontend directory
cd frontend

# Install packages
npm install
```

### 3. Configure Environment Variables
Create a `.env` file in the root of the `frontend/` directory (you can copy `.env.example` if available):
```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### 4. Start Development Server
```bash
npm run dev
```
The application will launch locally at `http://localhost:5173`.

### 5. Production Build
To create an optimized production build of the static site assets:
```bash
npm run build
```
The output assets will be saved to the `dist/` directory, ready to be hosted on Netlify, Vercel, or static web servers.

---

## 🔑 Core Features & Navigation Flows

1. **Authentication Guard**: Unauthenticated users trying to hit internal pages like `/dashboard` or `/compare` are intercepted by the `ProtectedRoute` component and redirected back to `/login`.
2. **Dynamic Snapshot Creation**: The `CreateSnapshot` page automatically pre-loads available industries and regions from the backend database to offer select menus.
3. **Data Availability Triggers**: If a user selects a region marked with `low` data availability, the detail view replaces the standard report button with a "Start Interview" prompt.
4. **Interactive AI Interview Wizard**: In `InterviewPage.jsx`, the user responds to a series of contextual questions. The frontend sends their response back to Django to trigger Gemini AI assessment calculations.
5. **Comparison Tool**: `ComparePage.jsx` renders side-by-side risk score panels, using filters to evaluate which business has the lower risk footprint.
