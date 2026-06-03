# RisCompass Frontend

A modern React + Vite frontend for the RisCompass risk assessment platform.

## 📦 Tech Stack

- **React 18** - UI library
- **Vite** - Fast build tool and dev server
- **Tailwind CSS** - Utility-first CSS framework
- **React Router** - Client-side routing
- **Axios** - HTTP client with interceptors
- **Recharts** - Chart library for data visualization

## 🗂️ Project Structure

```
frontend/
├── src/
│   ├── components/           # Reusable React components
│   │   ├── Navbar.jsx        # Navigation bar
│   │   ├── ProtectedRoute.jsx # Authentication guard
│   │   └── LoadingSpinner.jsx # Loading indicator
│   ├── context/              # React Context for state management
│   │   └── AuthContext.jsx   # Authentication context
│   ├── pages/                # Page components
│   │   ├── Login.jsx         # Login page
│   │   ├── Register.jsx      # Registration page
│   │   └── Dashboard.jsx     # Dashboard with charts
│   ├── styles/               # Global styles
│   │   └── index.css         # Tailwind + custom utilities
│   ├── utils/                # Utility functions
│   │   └── api.js            # Axios instance with interceptors
│   ├── App.jsx               # Main app with routing
│   └── main.jsx              # Entry point
├── public/                   # Static assets
├── index.html                # HTML template
├── package.json              # Dependencies
├── vite.config.js            # Vite configuration
├── tailwind.config.js        # Tailwind CSS configuration
├── postcss.config.js         # PostCSS configuration
└── .env.example              # Environment variables template
```

## 🚀 Getting Started

### Prerequisites

- Node.js 24.16.0 LTS and npm

### Installation

```bash
cd frontend
npm install
```

### Environment Setup

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

Then update it with your API base URL:

```env
VITE_API_BASE_URL=http://localhost:8000/api
```

### Development Server

```bash
npm run dev
```

The frontend will be available at `http://localhost:5173`

### Build for Production

```bash
npm run build
```

Output will be in the `dist/` folder.

### Preview Production Build

```bash
npm run preview
```

## 🔑 Key Features

### Authentication

- **AuthContext** manages user state globally
- JWT tokens stored in localStorage
- Automatic token refresh on 401 errors
- Protected routes redirect unauthenticated users to login

### API Integration

- **Axios instance** with interceptors for:
  - Automatic token injection
  - Token refresh on expiry
  - Error handling

### UI Components

- **Navbar**: Responsive navigation with user info and logout
- **ProtectedRoute**: Guards routes from unauthorized access
- **LoadingSpinner**: Elegant loading state indicator
- **Custom Tailwind utilities**: Pre-styled buttons, inputs, cards

### Dashboard

- Welcome message personalized with user name
- Stats cards showing key metrics
- Line chart for risk trends
- Bar chart for assessments overview
- Placeholder section for recent risks

## 🎨 Tailwind CSS Customization

Custom colors and utilities are defined in `tailwind.config.js` and `src/styles/index.css`:

- Primary color: `#3b82f6` (blue)
- Secondary color: `#10b981` (green)
- Danger color: `#ef4444` (red)
- Warning color: `#f59e0b` (amber)

### Available CSS Classes

```css
.btn-primary      /* Primary button */
.btn-secondary    /* Secondary button */
.btn-outline      /* Outline button */
.input-field      /* Styled input */
.card             /* Card container */
.section          /* Page section with max-width */
```

## 📝 Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `VITE_API_BASE_URL` | `http://localhost:8000/api` | Backend API base URL |

## 🔗 API Endpoints Expected

The frontend expects the backend to provide these endpoints:

- `POST /auth/login/` - Login user
- `POST /auth/register/` - Register new user
- `POST /auth/token/refresh/` - Refresh access token

Adjust the endpoints in `src/utils/api.js` if your backend uses different paths.

## 📚 Adding New Pages

1. Create a new component in `src/pages/`
2. Add a route in `src/App.jsx`:

```jsx
<Route path="/your-page" element={<YourPage />} />
```

3. For protected pages, wrap with `<ProtectedRoute>`:

```jsx
<Route
  path="/protected-page"
  element={
    <ProtectedRoute>
      <ProtectedPage />
    </ProtectedRoute>
  }
/>
```

## 📚 Adding New Components

1. Create component in `src/components/`
2. Use Tailwind classes for styling
3. Import and use in pages

Example:

```jsx
// src/components/Card.jsx
export default function Card({ title, children }) {
  return (
    <div className="card">
      <h3 className="font-bold mb-4">{title}</h3>
      {children}
    </div>
  )
}
```

## 🐛 Troubleshooting

### Port already in use

Change the port in `vite.config.js`:

```js
server: {
  port: 3000, // Change to another port
}
```

### API calls failing

1. Check `VITE_API_BASE_URL` in `.env`
2. Ensure backend is running
3. Check browser console for CORS errors

### Styling not applying

- Ensure Tailwind classes are spelled correctly
- Run `npm run build` if using production build
- Clear browser cache

## 📞 Support

For issues, check the main RisCompass README or contact the development team.
