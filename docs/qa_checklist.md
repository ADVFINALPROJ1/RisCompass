# RisCompass Manual QA Checklist

This document provides a comprehensive checklist for manually verifying the functionality, routing, security, and user experience of RisCompass.

## 1. Authentication & Security
- [ ] **User Registration**
  - Navigate to the registration page (`/register`).
  - Verify that leaving fields empty shows validation errors.
  - Verify registering with mismatching passwords shows an error.
  - Verify registering with an existing email shows a server-side error.
  - Verify successful registration redirects to the `/login` page or automatically logs the user in.
- [ ] **User Login**
  - Navigate to the login page (`/login`).
  - Enter invalid credentials and check for correct error messages.
  - Enter valid registered credentials and verify successful login.
  - Check that a JWT access token and refresh token are stored in localStorage/sessionStorage.
  - Verify redirect to `/dashboard` upon successful login.
- [ ] **Unauthorized Access Protection**
  - Log out of the system.
  - Attempt to access `/dashboard` directly via the browser address bar.
  - Attempt to access `/snapshots/create` directly.
  - Attempt to access `/reports/:id` or `/compare` directly.
  - Verify that the app blocks access and redirects to `/login` (route protection via `ProtectedRoute`).
- [ ] **JWT Protected API Routes**
  - Using developer tools (Network tab) or Postman, verify that API endpoints (e.g., `/api/snapshots/`, `/api/v1/external-data/`) return `401 Unauthorized` when accessed without a valid `Authorization: Bearer <token>` header.
  - Verify that the access token successfully accesses these endpoints when attached.
- [ ] **User Logout**
  - Click the "Logout" button in the navigation bar.
  - Verify that the JWT tokens are cleared from the storage.
  - Verify immediate redirection to the `/login` page.
  - Try to hit the back button and verify that dashboard content is not accessible.

## 2. Business Snapshot Management
- [ ] **Create Business Snapshot**
  - Navigate to the Snapshot Studio (`/snapshots/create` or click "New Snapshot" from Dashboard).
  - Fill out the snapshot creation form:
    - Title: "Berlin Tech Cafe"
    - Description: "A trendy coffee shop in the heart of Berlin featuring tech-themed spaces."
    - Industry: Select **Tech** (or **Retail** / **Service**)
    - Region: Select **Berlin** (Germany)
    - Business Stage: Select **Startup** (or **Idea**)
    - Startup Budget: Enter `120000`
    - Target Customer: "Tech workers, students, coffee enthusiasts"
    - Business Size: Select **Micro**
    - Check "I have a physical business location"
  - Click "Create Snapshot".
  - Verify successful creation and redirect to `/dashboard`.
- [ ] **Dashboard Snapshot List**
  - Verify that the newly created snapshot appears as a card in the dashboard snapshot grid.
  - Check that the snapshot title, industry, region, and creation date are rendered correctly.
  - Verify that clicking "View Details" on the card routes to `/snapshots/:id`.

## 3. Risk Report Generation & Analysis
- [ ] **Generate Report for Berlin Tech Cafe**
  - Select the "Berlin Tech Cafe" snapshot from the dashboard.
  - Under Snapshot Details, verify that "Generate Risk Report" button is visible (no interview is triggered because Berlin is a supported urban region with High data availability).
  - Click "Generate Risk Report".
  - Verify that the app displays a loading state and successfully generates the report.
  - Verify that the overall risk score, category risk scores (Financial, Market, Legal, Cultural, Operational), summary, and recommendations are displayed.
- [ ] **Confidence Gauge & Risk Factors**
  - On the generated Berlin Tech Cafe report page:
    - Verify that the **Confidence Gauge** displays a high confidence score (e.g., above 80%) with a label like "High" (reflecting high data availability in Berlin).
    - Verify that the **Risk Radar Chart** or breakdown shows scores for all 5 categories.
    - Verify that individual **Risk Factors** list names, scores, explanations, and their source types (e.g., "External API" or "System Default").
- [ ] **Generate Report for Remote Ethiopia Agriculture (AI Interview Trigger)**
  - Create a new snapshot:
    - Title: "Remote Ethiopia Agriculture"
    - Description: "An agricultural cooperative project in rural Ethiopia focused on sustainable crops."
    - Industry: Select **Agriculture**
    - Region: Select **Remote Ethiopia Region** (or a low-data region)
    - Business Stage: Select **Idea**
    - Startup Budget: `50000`
    - Target Customer: "Local markets, wholesale buyers"
    - Business Size: Select **Small**
    - Checkbox: Leave "Physical location" unchecked
  - Click "Create Snapshot".
  - Navigate to the "Remote Ethiopia Agriculture" details page.
  - Verify that the system detects low data availability and prompts with an **AI Interview Session** card ("Start Interview" or similar) instead of the immediate report generation.
- [ ] **Submit Interview Answers**
  - Click "Start Interview" on the snapshot detail page.
  - Verify the step-by-step interview interface loads questions tailored to the agriculture industry and remote regions.
  - Provide text answers or scale values for the questions.
  - Click "Submit Answers" at the end of the interview.
  - Verify that the status updates to "Generating AI-assisted report...".
- [ ] **Final Report After Interview**
  - Verify redirect to the completed risk report page for the Remote Ethiopia Agriculture snapshot.
  - Check that the **Confidence Gauge** shows an updated confidence score (e.g., lower than Berlin but boosted by the user's interview answers).
  - Verify that the AI-generated local insights, risk signals, and customized warnings are integrated into the final report.

## 4. Comparison Tool
- [ ] **Run Comparison**
  - Navigate to the Comparison page (`/compare` or click "Compare" in the navigation bar).
  - Select Snapshot A: "Berlin Tech Cafe"
  - Select Snapshot B: "Remote Ethiopia Agriculture"
  - Select a focus filter (e.g., "Overall", "Financial", or "Market").
  - Click "Compare" or let it live update.
  - Verify that the comparison page renders a side-by-side card structure.
  - Check that it correctly highlights the "Winner" (lower overall risk/better outlook) based on the focus filter.
  - Verify that the summary of the comparison is clearly visible and readable.
