# RisCompass 5-Minute Demo Script

This script walks through a live demonstration of RisCompass, highlighting key features, regional/industry differences, and the AI interview capability.

---

## Part 1: Introduction & Authentication (0:00 - 1:00)

**Speaker Dialogue:**
> "Welcome to RisCompass, our full-stack risk assessment platform designed to help entrepreneurs evaluate and compare business risks across different industries and geographic regions. 
> 
> Let's start by logging in. I will enter my credentials to log into my account. If we didn't have one, we could easily register. Our authentication is secured using JSON Web Tokens (JWT) on the Django REST Framework backend."

**Actions:**
1. Navigate to `http://localhost:5173/login`.
2. Enter a test email (e.g., `student@example.com`) and password (`SecurePass123`).
3. Click **Login** and point out the redirection to the `/dashboard`.

---

## Part 2: High-Data Region: Berlin Tech Cafe (1:00 - 2:00)

**Speaker Dialogue:**
> "Now that we are on the dashboard, we see a list of our existing business snapshots. Let's create a new snapshot for a retail/tech venture in a high-data-availability region: a Tech Cafe in Berlin, Germany."

**Actions:**
1. Click **New Snapshot** or navigate to `/snapshots/create`.
2. Fill in the form:
   - **Title**: `Berlin Tech Cafe`
   - **Description**: `A hybrid space combining high-quality coffee with shared workspaces for software engineers and digital creators.`
   - **Industry**: Select `Tech` (or `Retail`/`Service` depending on what's configured)
   - **Region**: Select `Berlin`
   - **Business Stage**: Select `Startup`
   - **Startup Budget**: `120000`
   - **Target Customer**: `Developers, remote workers, students`
   - Check the **Physical location** checkbox.
3. Click **Create Snapshot**.
4. In the dashboard, click **View Details** on the new "Berlin Tech Cafe" card.
5. Point out that because Berlin is a supported, high-data-availability region, we can generate a report immediately. Click **Generate Risk Report**.
6. Show the resulting report page, showing a high **Confidence Score** (e.g., 90% "High") and the category-wise risk radar chart.

---

## Part 3: Low-Data Region & AI Interview: Remote Ethiopia Agriculture (2:00 - 3:45)

**Speaker Dialogue:**
> "But what happens if we are planning a business in a remote region where external APIs like the World Bank have limited data? Let's create a second snapshot: a sustainable agriculture project in Remote Ethiopia."

**Actions:**
1. Click **Dashboard** and then **New Snapshot**.
2. Fill in the form:
   - **Title**: `Ethiopia Sustainable Farms`
   - **Description**: `An agricultural cooperative in rural Ethiopia utilizing sustainable farming practices to cultivate local crops for regional markets.`
   - **Industry**: Select `Agriculture`
   - **Region**: Select `Remote Ethiopia Region`
   - **Business Stage**: Select `Idea`
   - **Startup Budget**: `45000`
   - **Target Customer**: `Local markets, regional food distributors`
   - Leave **Physical location** unchecked.
3. Click **Create Snapshot** and click **View Details** on the new "Ethiopia Sustainable Farms" card.
4. Point out that the system detects a lower data availability level, triggering the **AI Interview Session** workflow to bridge the information gap.
5. Click **Start Interview**.
6. Walk through and answer the generated questions (e.g., questions about water source, logistics, local regulatory permits).
   - *Example answer*: "We rely on seasonal rainfall and a local cooperative borehole."
   - *Example scale*: Select moderate-to-high risk levels where appropriate.
7. Click **Submit Answers**.
8. Show the completed report page. Explain that the AI (powered by the Gemini API) analyzed the user's custom interview answers and combined it with default weights to construct a customized risk assessment.

---

## Part 4: Comparative Analysis & Confidence Gauge (3:45 - 5:00)

**Speaker Dialogue:**
> "Now let's compare our two business snapshots side-by-side to understand which venture has a lower risk profile and how our data confidence varies.
> 
> As we look at the comparison page, we can see a side-by-side analysis of Berlin Tech Cafe vs. Ethiopia Sustainable Farms.
> 
> Notice the **Confidence Gauge** difference. The Berlin project has a high confidence score because of rich, reliable historical and economic indicators from the region. The Ethiopia project has a lower confidence score, but it has been significantly improved and enriched thanks to the AI-assisted interview answers.
> 
> We can filter by different risk dimensions—like Financial Risk or Legal Risk—to see which project stands out as the safer option for our portfolio."

**Actions:**
1. Click **Compare** in the navigation bar.
2. Select Snapshot A: `Berlin Tech Cafe` and Snapshot B: `Ethiopia Sustainable Farms`.
3. Toggle the focus filters (Overall, Financial, Market, Legal) and highlight how the winner changes.
4. Point out the confidence gauge difference and summarize the results.
5. Conclude the presentation.
