# Weather-Driven Business Intelligence Platform
## Complete Project Report — From Zero to Everything

> **How to read this:** Think of this document as your personal tour guide. We start from the very basics — what is a line of code, why does weather affect revenue — and build all the way up to how every file and system in this project works. No prior programming or data science knowledge is required.

---

## Part 1 — The Big Idea (What Is This Project?)

### In one sentence
This project is an **enterprise-grade, real-time business intelligence platform** that answers one question every executive and business owner secretly wants to know:

> *"How much money am I losing (or gaining) because of today's weather — and what should I do about it right now?"*

### The analogy
Imagine you own 10 businesses across a major city: a food delivery fleet, a bike-share network, an indoor cinema, a beachfront cafe, a car wash, and a rideshare service.

On a rainy Tuesday evening, some of those businesses will boom (food delivery surges, rideshare prices spike, indoor cinema seats fill up) while others will plummet (bike rentals freeze, outdoor dining shuts down, car washes sit completely empty).

The critical questions are:
1. **By exactly how many dollars?**
2. **Which weather variable caused the shift — precipitation, temperature anomaly, or wind?**
3. **Can we predict this 7 days in advance so managers can staff up or trim supply chains before the storm arrives?**

That is precisely what this platform computes — live, for any major metropolitan area, any business portfolio, and today's actual weather conditions.

### Dual Presentation Architecture
To deliver maximum reliability, performance, and flexibility, the platform operates in two distinct, complementary environments:

1. **Production Standalone Web Application:** A dedicated, lightweight web application powered by Python Flask on the backend, with a reactive HTML5, CSS3, modern JavaScript, and Plotly.js interface. It runs asynchronously in any browser with instant responsiveness, zero full-page reload flickering, and custom-tailored executive styling.
2. **Preserved Local Backup Dashboard:** A complete, self-contained Streamlit application kept safely on disk as an operational backup and rapid offline prototyping environment.

---

## Part 2 — Core Vocabulary (Every Term Explained)

### Programming & Software Terms

| Term | What it Means in Plain English |
|:---|:---|
| **Python** | The programming language this entire project is written in. Think of it as the grammar and vocabulary we use to give step-by-step instructions to the computer. |
| **Library / Package** | A collection of pre-written code created and shared by software engineers so others do not have to reinvent the wheel. Like buying a pre-assembled LEGO motor rather than molding plastic gears yourself. |
| **Function** | A named block of code that does one specific job. Like a culinary recipe: you call it by name, pass in raw ingredients (arguments), and it returns a finished dish (result). |
| **API** | *Application Programming Interface.* A standardized doorway through which two software programs talk to each other across the internet. Like a waiter at a restaurant: you give your order (request) and receive food back (response/data). |
| **REST API & Endpoints** | A web service organized around specific web addresses called "endpoints." Like numbered service windows at a post office: window `/api/weather` provides weather data, while window `/api/domino` provides economic cascade calculations. |
| **Client-Server Architecture** | A division of labor where the "Server" (Flask in Python) handles heavy math, file loading, and database queries in the background, while the "Client" (your web browser) displays the visual buttons, cards, and charts. |
| **Single-Page Application (SPA)** | A modern web design where the entire page loads once. When you click a button or change a slider, only the specific chart or card updates behind the scenes without the whole browser flashing or reloading. |
| **DOM & JavaScript** | The *Document Object Model* (DOM) is the tree of visual elements on a web page. JavaScript is the programming language running inside your browser that listens for mouse clicks and modifies those elements on the fly. |
| **Flask** | A fast, minimalist Python web framework that listens for browser requests and responds with JSON data or HTML pages. |
| **JSON** | *JavaScript Object Notation.* A universal, human-readable text format for sending structured data across the web. It looks like a labeled dictionary: `{"city": "New York", "temperature_c": 18.5}`. |
| **DataFrame** | A two-dimensional table of data in Python — identical to a spreadsheet with rows and columns, but managed with high-speed computational code via Pandas. |
| **Parquet File** | A modern, highly compressed, column-oriented file format for storing large datasets on disk. It loads up to 10 times faster than CSV and uses a fraction of the disk space. |
| **CSV File** | *Comma-Separated Values.* A plain-text table format where each line represents a row and columns are separated by commas. |
| **Class** | An architectural blueprint for creating custom objects in Python. Like an architectural floor plan: you draw the blueprint once, then construct multiple real buildings from it. |
| **Repository (Repo)** | A specialized folder tracked by Git that contains all project files along with a permanent, cryptographic ledger of every modification ever made. |

### Data Science & Econometric Terms

| Term | What it Means in Plain English |
|:---|:---|
| **Dataset** | A structured collection of observations. In this platform: 2 years of hourly weather telemetry merged with 21 business operational metrics across 4 metropolitan areas. |
| **EDA** | *Exploratory Data Analysis.* The systematic investigation of data tables using summary statistics and visualizations to discover patterns before building statistical models. |
| **Feature** | A measurable explanatory input in a dataset. Examples: `precipitation_mm`, `temp_anomaly_deg_c`, `wind_speed_kmh`. |
| **Target Variable** | The outcome variable we want to understand or forecast. Examples: daily gross revenue, food delivery order volume, bike-share rental counts. |
| **Elasticity** | A percentage-based measure of sensitivity. An elasticity of `+0.035` for rain means that for every additional 1 millimeter of rainfall, business volume increases by exactly 3.5%. |
| **Regression** | A mathematical technique that calculates the best-fitting quantitative relationship between input drivers (weather conditions) and output results (business revenue). |
| **Coefficient** | The multiplier calculated by a regression model. A coefficient of `+180` for precipitation means that each additional millimeter of rain adds 180 food delivery orders. |
| **R-squared (R²)** | A statistical metric between 0.0 and 1.0 (0% to 100%) indicating how much of the variation in business volume is successfully explained by the model. |
| **P-value** | A statistical confidence check. A p-value below 0.01 indicates there is less than a 1% probability that the observed relationship occurred by pure random chance. |
| **Anomaly** | A departure from normal seasonal expectations. An afternoon temperature of 8°C in mid-July is a negative temperature anomaly (unseasonably cold). |
| **Correlation** | The degree to which two variables move together. If rain and indoor cinema ticket sales rise at the same time, they are positively correlated. |
| **Confounder** | A hidden third variable that creates a false appearance of cause and effect. For instance, Friday evenings have both high rain and high restaurant sales in a sample, but people eat out because it is Friday, not because it is raining. |
| **TWFE** | *Two-Way Fixed Effects.* An econometric panel regression technique that isolates true causal impacts by simultaneously removing calendar variations and permanent city differences. |
| **HC1 Robust Errors** | *Heteroscedasticity-Consistent Standard Errors.* A statistical correction that ensures confidence intervals remain valid even when data variability changes during extreme weather storms. |

### Weather & Meteorology Terms

| Term | What it Means in Plain English |
|:---|:---|
| **WMO Code** | *World Meteorological Organization Weather Code.* A standardized universal number describing sky and atmospheric conditions (e.g., Code 0 = Clear Sky; Code 65 = Heavy Rain; Code 95 = Thunderstorm). |
| **Precipitation** | Any moisture falling from the atmosphere to the earth, including rain, drizzle, snow, and hail. Quantified in millimeters (mm). |
| **NASA POWER** | *Prediction of Worldwide Energy Resources.* NASA's satellite-derived solar and meteorological database, offering spaceborne surface measurements across the globe. |
| **Open-Meteo** | A high-performance, open-source global weather API that delivers real-time ground-station telemetry and 7-day numerical forecasts. |
| **NASA Worldview** | An interactive satellite imagery browser operated by NASA that allows visual inspection of actual cloud formations and weather fronts from orbit. |
| **GIBS** | *Global Imagery Browse Services.* The distributed server architecture NASA uses to deliver full-resolution satellite imagery tiles across the web. |

---

## Part 3 — The Technology Stack (What Tools We Used and Why)

### System Architecture Overview

```
┌───────────────────────────────────────────────────────────────────────────────────┐
│                           WHAT THE USER EXPERIENCES                               │
│       Modern Responsive Browser Interface (HTML5 + CSS3 + Vanilla ES6 JS)          │
│                High-Performance Non-Zoomable Charts (Plotly.js)                    │
├───────────────────────────────────────────────────────────────────────────────────┤
│                        APPLICATION & API SERVICE LAYER                            │
│           Flask REST API Server (server.py)  [Port 5000 / Web Application]        │
│          Streamlit Operational Backup (app.py)  [Port 8501 / Local Fallback]      │
├───────────────────────────────────────────────────────────────────────────────────┤
│                             ANALYTICS & BUSINESS BRAIN                            │
│          revenue_analytics.py   |   econometrics.py   |   live_weather.py         │
│          revenue_connectors.py  |   data_pipeline.py  |   data_generator.py       │
├───────────────────────────────────────────────────────────────────────────────────┤
│                             DATA SCIENCE FOUNDATIONS                              │
│         Pandas   |   NumPy   |   SciPy   |   Statsmodels   |   PyArrow            │
├───────────────────────────────────────────────────────────────────────────────────┤
│                             EXTERNAL TELEMETRY FEEDS                              │
│       Open-Meteo API   |   NASA POWER API   |   Square POS   |   Stripe API       │
└───────────────────────────────────────────────────────────────────────────────────┘
```

---

### Library-by-Library Breakdown

#### `Flask` — The Production Web Application Framework
- **What it is:** A lightweight, robust Python framework designed for routing web traffic, executing server-side logic, and serving REST API endpoints.
- **Why we chose it:** Traditional monolithic frameworks introduce heavy overhead. Flask provides direct control over HTTP request handling, asynchronous JSON serialization, and static asset distribution without unnecessary background baggage.
- **Role in platform:** Hosts the 8 REST endpoints in `website/server.py` and delivers the single-page application to the browser.
- **Version used:** `>= 2.2.0`

#### `HTML5, CSS3 & Modern JavaScript` — The Frontend Engine
- **What they are:** The native languages of the World Wide Web. HTML5 structures the page, CSS3 handles layout and colors, and JavaScript controls real-time responsiveness.
- **Why we chose them:** By avoiding massive JavaScript build frameworks (like heavy React or Angular toolchains), the frontend loads instantly, requires zero build step (no npm compilation), and runs smoothly on any modern desktop or mobile browser.
- **Role in platform:** Powers `website/templates/index.html`, `website/static/css/style.css`, and `website/static/js/app.js`. Listens for user interactions, calls Flask API endpoints via `fetch()`, and updates the dashboard without reloading the page.

#### `Plotly` & `Plotly.js` — The Executive Chart Engine
- **What they are:** Advanced interactive data visualization engines available for both Python and JavaScript.
- **Why we chose them:** Plotly generates sharp vector graphics with rich hover tooltips, smooth animations, and multi-series overlays.
- **Customizations applied:**
  - **Non-overlapping axis geometry:** Left margin set to 85 pixels and title standoff set to 18 pixels so currency labels (e.g., `$100k`, `$250k`) never collide with rotated axis titles.
  - **Locked non-zoomable interaction:** Disabled mouse scroll zoom and box zoom (`fixedrange: true`, `scrollZoom: false`) to keep executive charts perfectly framed and stable during mouse interactions.
- **Version used:** Python `plotly >= 5.15.0`; JavaScript `plotly-2.27.0.min.js`.

#### `Streamlit` — The Preserved Operational Backup
- **What it is:** A Python framework that automatically converts Python scripts into interactive browser tools.
- **Role in platform:** Kept as a complete, fully functioning local backup in `app.py`. If a user wants to run an offline demonstration or perform rapid algorithm prototyping without launching a separate web server, Streamlit provides a single-command fallback (`streamlit run app.py`).
- **Version used:** `>= 1.30.0`

#### `Pandas` — The Tabular Data Workhorse
- **What it is:** The foundational Python library for working with structured data tables.
- **Role in platform:** Manages dataset loading, column transformations, date parsing, timezone harmonizations, rolling averages, and metric aggregations across the entire pipeline.
- **Version used:** `>= 2.1.0`

#### `NumPy` & `SciPy` — Scientific & Mathematical Foundations
- **What they are:** High-performance libraries for numerical computation, matrix algebra, and scientific statistical functions.
- **Role in platform:** Powers the mathematical simulation of seasonal temperatures using trigonometric cycles (`np.cos`), introduces stochastic weather front shocks, and calculates matrix operations for regression models.
- **Version used:** `numpy >= 1.23.0`, `scipy >= 1.10.0`

#### `Statsmodels` — The Econometric Estimation Engine
- **What it is:** A specialized Python library for rigorous statistical modeling and econometrics.
- **Role in platform:** Estimates the Two-Way Fixed Effects panel regressions using Ordinary Least Squares with White HC1 heteroscedasticity-robust covariance matrices (`cov_type="HC1"`).
- **Version used:** `>= 0.14.0`

#### `PyArrow` — High-Performance File Serialization
- **What it is:** A cross-language development platform for in-memory columnar data that provides read/write access to Apache Parquet files.
- **Role in platform:** Stores the aligned 70,000+ record historical dataset on disk in `data/processed/`.
- **Version used:** `>= 12.0.0`

#### `Pytest` — Automated Quality Verification
- **What it is:** An automated testing framework for Python.
- **Role in platform:** Automatically executes unit and integration tests in `tests/test_connectors.py` and `tests/test_pipeline.py` to ensure zero regressions occur when code is modified.
- **Version used:** `>= 7.4.0`

---

## Part 4 — How Each File Works (The Code Explained)

### Project File Structure

```
weather-business-impact-eda/
│
├── website/                               ← Standalone Production Web Application
│   ├── server.py                          ← Flask REST API backend (Port 5000)
│   ├── templates/
│   │   └── index.html                     ← Semantic 5-tab single-page interface
│   └── static/
│       ├── css/
│       │   └── style.css                  ← Obsidian Dark theme & responsive styling
│       └── js/
│           └── app.js                     ← Asynchronous client controller & Plotly.js logic
│
├── run_website.bat                        ← 1-click Windows launcher for web application
├── app.py                                 ← Preserved Local Streamlit backup dashboard
│
├── src/                                   ← Reusable Analytics & Data Engine Modules
│   ├── data_generator.py                  ← Mathematical simulator for historical data
│   ├── data_pipeline.py                   ← Data cleaning, timezone alignment & Parquet storage
│   ├── econometrics.py                    ← Two-Way Fixed Effects regression models
│   ├── live_weather.py                    ← Real-time telemetry from Open-Meteo & NASA POWER
│   ├── revenue_analytics.py               ← Business impact calculations, dominoes & nowcasting
│   ├── revenue_connectors.py              ← Square POS, Stripe & CSV transaction connectors
│   └── visualizer.py                      ← Matplotlib & Seaborn static chart generator
│
├── tests/                                 ← Automated Test Suite (7 passing tests)
│   ├── test_connectors.py                 ← Validates Square, Stripe & CSV connectors
│   └── test_pipeline.py                   ← Validates data generation, shapes & econometrics
│
├── data/                                  ← Historical Data Repositories
│   ├── raw/                               ← Original unaligned CSV exports
│   └── processed/                         ← Cleaned, aligned Apache Parquet tables
│
├── reports/                               ← Project Documentation & Export Artifacts
│   ├── project_report.md                  ← Comprehensive markdown project report
│   ├── project_report.pdf                 ← Professional enterprise PDF report
│   └── build_pdf_report.py                ← Automated script for PDF compilation
│
├── requirements.txt                       ← Complete Python library dependency specifications
├── .streamlit/config.toml                 ← Theme configuration for backup Streamlit dashboard
├── .gitignore                             ← Git ignore rules (protecting local caches & backups)
└── README.md                              ← Repository overview and quickstart guide
```

---

### File 1: `src/data_generator.py` — The Synthetic Data Factory

**Purpose:** Synthesizes realistic, high-frequency historical weather and business performance data from mathematical first principles.

**Why it is needed:** To rigorously train econometric models across multiple cities, an analyst requires several continuous years of hourly multi-variate weather metrics aligned with granular point-of-sale business data. Licensing commercial datasets of this depth across multiple metropolitan markets can cost tens of thousands of dollars. We solved this by developing a rigorous mathematical generator that mirrors real-world meteorological thermodynamics and microeconomic behavior.

**Step-by-step operation:**
1. **Seasonal Temperature Baseline:** Computes a cyclical annual temperature baseline using a cosine wave parameterized by the day of the year (`cos(2 * pi * day_of_year / 365.25)`). Winter represents the annual trough and summer represents the peak.
2. **Atmospheric Front Shocks:** Overlays stochastic cold fronts, heatwaves, and seasonal temperature anomalies on top of the smooth cosine baseline.
3. **Storm & Precipitation Generator:** Simulates precipitation using a Markov-like storm arrival process. When a rain event triggers, it follows a gamma-distributed intensity curve with realistic storm duration and runoff decay.
4. **Microeconomic Sector Drivers:** For each of 21 business operational metrics, computes demand shifts by multiplying baseline volumes by weather sensitivity functions.
5. **Real-World Distortion Layer:** Injects realistic sensor anomalies, missing hourly readings, and local timestamp offsets to simulate real-world data collection challenges.

---

### File 2: `src/data_pipeline.py` — The Multi-Source Data Harmonizer

**Purpose:** Ingests unaligned, asynchronous raw datasets from multiple sources and compiles them into a single, analysis-ready Parquet dataset.

**Core Data Engineering Challenges Solved:**

| Technical Challenge | Root Cause in Raw Data | Engineering Solution Implemented |
|:---|:---|:---|
| **Timestamp Mismatches** | Weather records use UTC; business transactions use local city time. | Normalized all timestamps to UTC using IANA timezone definitions. |
| **Sampling Frequency Disparity** | Weather sensors sample hourly; POS transactions record every 15 minutes. | Resampled and aggregated transaction records up to uniform 1-hour intervals. |
| **Missing Telemetry Gaps** | Sensor dropouts and network transmission disconnects. | Implemented forward-fill (`ffill`) followed by backward-fill (`bfill`) imputation. |
| **Multi-City Alignment** | 4 distinct geographic regions with different calendar shifts. | Applied city-specific coordinate and timezone mapping tables. |

**Output & Engineered Features:**
- Output: `data/processed/aligned_weather_business.parquet` (70,000+ rows, 40+ attributes).
- `temp_anomaly_deg_c`: Difference between current temperature and the 30-day rolling seasonal expectation.
- `precip_tier`: Categorical classification (`None`, `Light`, `Moderate`, `Heavy`, `Extreme`).
- `is_holiday`: Boolean indicator identifying official public holidays.
- Calendar controls: `hour_of_day`, `day_of_week`, and `month`.

---

### File 3: `src/econometrics.py` — The Econometric Intelligence Engine

**Purpose:** Runs Two-Way Fixed Effects (TWFE) panel regressions to isolate true causal weather elasticities from seasonal and calendar confounders.

#### Why Naive Correlation Fails
Suppose an analyst notices that food delivery order volume is high on rainy Friday evenings. A naive correlation analysis might conclude that rainfall causes an 80% surge in orders. However, Friday evenings experience massive order volume regardless of weather. Treating the entire surge as weather-driven is a severe statistical error caused by calendar confounding.

#### How Two-Way Fixed Effects Solves Confounding
The TWFE regression model mathematically deconstructs observed variation into separate component bins:
- City fixed effects (`C(metro_area)`): Controls for permanent differences between cities (e.g., New York is denser than Phoenix).
- Hour fixed effects (`C(hour_of_day)`): Controls for daily meal times and commuter rush hours.
- Day-of-week fixed effects (`C(day_of_week)`): Controls for weekend vs. weekday habits.
- Month fixed effects (`C(month)`): Controls for annual macro-seasonality.
- Holiday fixed effects (`C(is_holiday)`): Controls for statutory holiday closures and celebrations.

#### Mathematical Specification:
```
Business_Metric = beta_rain * Precipitation_mm
                + beta_snow * Snowfall_cm
                + beta_temp * Temp_Anomaly_C
                + beta_wind * Wind_Speed_kmh
                + City_Effects + Hour_Effects + DayOfWeek_Effects
                + Month_Effects + Holiday_Effects + Residual
```

Once all fixed effects are held constant, the remaining coefficients (`beta`) capture the pure, isolated causal impact of each weather unit. All standard errors are adjusted using White's heteroscedasticity-robust covariance estimator (`HC1`).

---

### File 4: `src/live_weather.py` — The Real-Time Telemetry Gateway

**Purpose:** Connects to live global meteorological APIs, executes cross-validation checks, and returns real-time conditions for any requested city.

**Integrated Telemetry Sources:**
1. **Open-Meteo API:** Provides ground-level hourly observations and 7-day numerical forecasts based on NOAA, ECMWF, and DWD models.
2. **NASA POWER API:** Provides spaceborne surface meteorology parameters measured by orbital satellites, including corrected precipitation (`PRECTOTCORR`) and 2-meter air temperature (`T2M`).
3. **NASA Worldview GIBS:** Generates direct imagery coordinates allowing users to visually inspect real-time orbital cloud cover.

**Data Consensus Verification:**
When telemetry is fetched, the module compares the ground-station temperature from Open-Meteo with the spaceborne temperature from NASA POWER. If the variance is within 2.5°C, the feed is validated as "High Data Agreement." If variance exceeds this threshold, the system flags moderate variance to alert the operator of potential atmospheric instability or microclimate effects.

---

### File 5: `src/revenue_connectors.py` — Enterprise Revenue Integrations

**Purpose:** Pulls live commercial transaction data from merchant processing platforms and estimates business-specific empirical elasticities.

**Supported Connectors:**
- **`SquareConnector`:** Interacts with Square's v2 Orders and Payments REST API via OAuth Bearer token authentication to aggregate daily gross sales and transaction volume.
- **`StripeConnector`:** Interfaces with Stripe's Charges and PaymentIntents API to compute daily Gross Merchandise Value (GMV).
- **`CSVRevenueConnector`:** Allows any business to upload custom CSV or Excel files. Uses fuzzy string matching to automatically map column headers (such as `Trans Date`, `Net Sales`, `Total Amount`) without requiring manual reformatting.
- **`estimate_empirical_elasticities()`:** Merges a merchant's actual transaction history with localized weather archives to learn custom sensitivity coefficients tailored to that exact enterprise.

---

### File 6: `src/revenue_analytics.py` — Business Impact, Dominoes & Nowcasting

**Purpose:** The central analytical calculation engine of the platform, containing sector catalogs, urban mobility dynamics, domino cascading algorithms, and forward-looking nowcasts.

**Key Components:**
- **`BUSINESS_CATALOG`:** Defines baseline daily revenues, baseline transaction sizes, and empirical weather elasticities across 16+ business sectors.
- **`CITY_DYNAMICS`:** Encodes localized urban characteristics for New York, Chicago, Seattle, Phoenix, and London (transit modal shares, pedestrian shelter availability, and infrastructure bottleneck thresholds).
- **`generate_dynamic_domino_cascade()`:** Synthesizes a 6-step causal ripple chain showing how an initial meteorological shock propagates through transit systems, foot traffic, commercial spending, supply chains, and emergency operations.
- **`generate_business_specific_domino_effects()`:** Computes granular 5-part operational cards (Trigger, Consumer Reaction, Financial Impact, Ripple Effect, Recommended Countermeasure) for every selected business.
- **`analyze_inter_business_linkages()`:** Quantifies revenue substitution flows where one business in the portfolio gains customers diverted from another (e.g., dining room closures diverting spending into food delivery apps).
- **`generate_forward_nowcast()`:** Projects forward 7-day financial performance by marrying 7-day meteorological forecast telemetry with econometric elasticity curves.

---

### File 7: `website/server.py` — The Production Flask REST API Backend

**Purpose:** Serves as the central server for the standalone web application, exposing 8 high-performance REST API endpoints and distributing the frontend assets.

**Why Flask was Chosen:**
In data science deployments, frontend tools often force entire Python scripts to rerun from top to bottom on every user click. Flask eliminates this issue by operating as an asynchronous service layer. It keeps the data science models and historical tables in memory, executing calculations only when an endpoint is called and returning compact JSON payloads.

**The 8 REST API Endpoints:**

| Endpoint Route | HTTP Method | Function & Return Data |
|:---|:---|:---|
| `/` | `GET` | Renders and delivers the primary single-page application (`index.html`). |
| `/api/initial_data` | `GET` | Delivers the complete business catalog, city lists, default selections, and baseline portfolio figures on initial page boot. |
| `/api/weather` | `GET` | Takes `?city=<name>` query parameters and returns live Open-Meteo telemetry, NASA satellite metrics, and consensus scores. |
| `/api/historical` | `GET` | Delivers 2-year weekly revenue time-series data, synchronized precipitation records, and TWFE econometric benchmark tables. |
| `/api/domino` | `POST` | Accepts the active business portfolio and current weather parameters; computes the 6-step domino cascade, tipping point thresholds, per-business cards, and substitution flows. |
| `/api/nowcast` | `POST` | Accepts custom scenario shock overrides or live forecast parameters; computes 7-day revenue projections and operational recommendations. |
| `/api/diagnostics` | `GET` | Returns data engineering harmonization metrics (records merged, missingness treated, timezone offsets) and sample pipeline records. |
| `/api/day_review` | `POST` | Computes historical day-in-review diagnostic explanations for a selected past calendar date. |

---

### File 8: Frontend Suite (`index.html`, `style.css`, `app.js`)

**Purpose:** Provides a responsive, zero-flicker executive user interface that communicates with the Flask server via asynchronous background requests.

**1. `website/templates/index.html` — Semantic Layout:**
- **Live Weather Ribbon:** Top bar displaying current temperature, precipitation, wind speed, humidity, weather condition description, and NASA consensus badge.
- **Executive Control Bar:** City selection dropdown, active business portfolio toggle pills, and live API status pill.
- **Tab Navigation Bar:** 5 dedicated analytical views:
  - *Tab 1: Live Intelligence & 7-Day Snapshot*
  - *Tab 2: Historical Trends & Seasonality*
  - *Tab 3: Business Interactions & Domino Chains*
  - *Tab 4: Live AI Operational Nowcast & Strategic Guidance*
  - *Tab 5: Multi-Source Data Wrangling Diagnostics*
- **Modal Windows:** Clean dialog overlays for custom CSV transaction imports and payment gateway credential configurations.

**2. `website/static/css/style.css` — Obsidian Dark Design System:**
- Implements an enterprise dark palette with `#0B0F19` deep obsidian background and `#111827` elevated surface cards.
- Electric cyan (`#38BDF8`) accent colors, vibrant emerald (`#00E676`) positive indicators, and coral red (`#FF5252`) risk badges.
- Clean typography using system native fonts (`-apple-system`, `Segoe UI`, `Roboto`), responsive CSS grid layouts, and custom-styled interactive form controls.

**3. `website/static/js/app.js` — Reactive Client Controller:**
- Uses the native browser `fetch()` API to communicate with Flask endpoints asynchronously.
- Maintains client-side state (current selected city, active business portfolio, scenario overrides).
- Constructs and renders responsive Plotly.js charts with custom theme templates, zero-overlap margins, and non-zoomable coordinate locks.
- Dynamically generates HTML DOM cards for domino cascades, tipping points, and operational recommendations without full-page reloads.

---

### File 9: `run_website.bat` — The One-Click Windows Launcher

**Purpose:** Automates the complete application startup workflow for Windows operators.

**How it works:**
1. Opens the Windows command line and navigates to the project root directory.
2. Verifies that the Python runtime is available in the system path.
3. Launches the Flask backend server (`python website/server.py`) on `http://localhost:5000`.
4. Waits briefly for the server socket to initialize, then automatically launches the default web browser to the application URL.

---

### File 10: `app.py` — The Preserved Local Streamlit Backup Dashboard

**Purpose:** Preserves the complete, self-contained 1,573-line Streamlit dashboard on local disk as an operational fallback and offline analytical tool.

**Why keeping a local backup is sound engineering:**
In mission-critical enterprise systems, relying on a single deployment mode introduces operational risk. By preserving `app.py` locally on the operator's machine, the team retains an immediate, single-command fallback tool (`streamlit run app.py`). If the operator needs to inspect the system offline without running a multi-tier web server, the Streamlit dashboard provides full functional redundancy. To keep the remote GitHub repository clean and focused on the production web platform, `app.py` is safely maintained locally and excluded from remote git tracking.

---

## Part 5 — The Data Flow (How Everything Connects)

```
STEP 1: DATA GENERATION (One-time setup)
data_generator.py synthesizes 2 years of multi-city weather and business records.
        │
        ▼
STEP 2: DATA PIPELINE (One-time processing)
data_pipeline.py harmonizes timezones, imputes missing values, and saves to Parquet.
        │
        ▼
STEP 3: ECONOMETRIC ENGINE (Executed on server boot)
econometrics.py loads Parquet records and computes TWFE regressions for 21 metrics.
        │
        ▼
STEP 4: LIVE TELEMETRY (Cached hourly)
live_weather.py fetches real-time feeds from Open-Meteo and NASA POWER.
        │
        ▼
STEP 5: REVENUE CONNECTORS (Initialized on boot)
revenue_connectors.py connects Square and Stripe feeds, estimating empirical elasticities.
        │
        ▼
STEP 6: BUSINESS INTELLIGENCE ENGINE (Calculated per request)
revenue_analytics.py computes domino chains, dollar shifts, and 7-day nowcasts.
        │
        ▼
STEP 7: STANDALONE PRODUCTION WEB INTERFACE (Default Mode)
Flask server.py serves endpoints -> browser app.js fetches JSON -> renders Plotly.js charts
[Instant asynchronous updates with zero full-page reload flickering]
        │
        ▼
STEP 7b: OPERATIONAL BACKUP INTERFACE (Fallback Mode)
app.py executes locally via Streamlit for offline single-process demonstration.
```

---

## Part 6 — The Automated Tests

**Why automated tests exist:** Whenever software is enhanced or refactored, there is a risk of introducing unintended bugs into existing algorithms. Automated test suites run programmed assertions that verify mathematical accuracy, data shapes, and API connectors after every change.

### Test Suite Summary (7 Passing Tests in ~19 Seconds)

**File: `tests/test_connectors.py`** — 4 Tests:

| Test Identifier | Verification Performed |
|:---|:---|
| `test_square_connector_sandbox` | Asserts that Square POS integration returns structured daily revenue and transaction counts matching schema specifications. |
| `test_stripe_connector_sandbox` | Asserts that Stripe payment integration generates valid Gross Merchandise Value (GMV) data structures. |
| `test_csv_revenue_connector_fuzzy` | Asserts that fuzzy column matching accurately recognizes non-standard column names (e.g., `Sales_USD`, `Event_Date`). |
| `test_empirical_elasticity_regression` | Asserts that econometric regression runs successfully on merchant transaction tables, yielding statistically bounded coefficients. |

**File: `tests/test_pipeline.py`** — 3 Tests:

| Test Identifier | Verification Performed |
|:---|:---|
| `test_data_generation_shapes` | Asserts that synthetic weather and business tables contain the exact expected row counts and required column fields. |
| `test_pipeline_alignment` | Asserts that the merged Parquet dataset has uniform hourly timestamps, zero timezone misalignment, and complete data integrity. |
| `test_econometric_scenario_simulation` | Asserts that econometric nowcasting functions produce mathematically consistent revenue projections under extreme weather shocks. |

---

## Part 7 — Live APIs and External Services

| Service Name | Provider & Endpoint | Access Model | Data Ingested into Platform |
|:---|:---|:---|:---|
| **Open-Meteo** | `api.open-meteo.com/v1/forecast` | Public / Free (No key needed) | Real-time ground station temperature, precipitation, wind speed, humidity, and 7-day numerical forecasts. |
| **NASA POWER** | `power.larc.nasa.gov/api/temporal` | Public / Free (NASA Earthdata) | Spaceborne satellite surface meteorology (solar radiation, precipitation, 2-meter air temperature). |
| **NASA Worldview** | `worldview.earthdata.nasa.gov` | Public / Free Browser URL | Direct visual satellite imagery feeds showing real-time cloud and weather systems. |
| **Square POS API** | `connect.squareup.com/v2/orders` | OAuth 2.0 Merchant Token | Point-of-sale restaurant and retail order counts and transaction totals. |
| **Stripe API** | `api.stripe.com/v1/charges` | Secret Key Authentication | Online merchant charge data and gross platform transaction volume (GMV). |

---

## Part 8 — Visual Design & Chart Geometry Decisions

### The Obsidian Dark Theme
- **Background Primary:** `#0B0F19` (Deep Obsidian Blue — prevents eye strain during extended analytical sessions).
- **Surface Elevation:** `#111827` (Card backgrounds providing clean visual hierarchy).
- **Primary Accent:** `#38BDF8` (Electric Cyan — highlights data signals, active controls, and navigation states).
- **Positive Shift:** `#00E676` (Vibrant Emerald — indicates revenue growth and favorable weather impacts).
- **Negative Shift:** `#FF5252` (Coral Red — highlights financial risk, supply chain bottlenecks, and severe storms).
- **Chart Traces:** `#FFFFFF` (Solid high-contrast white lines with 3.0px width for maximum legibility).
- **Zero Emojis:** Strictly maintained clean, corporate, executive typography throughout all headings, cards, and labels.

### Chart Geometry & Axis Overlap Prevention
In financial dashboards displaying multi-digit currency amounts (e.g., `$100,000`, `$250k`), standard chart margins often cause the rotated vertical axis title ("Revenue ($ USD)") to collide directly into the numeric tick labels, creating an illegible visual overlap.

**Our Geometric Solution:**
1. **Left Margin Expansion:** Increased the chart container left margin to a generous `85px` (`margin: { l: 85, r: 35, t: 30, b: 50 }`).
2. **Title Standoff Separation:** Configured an explicit standoff distance of `18px` on the y-axis title (`title: { text: "...", standoff: 18 }`).
3. **Automargin Activation:** Enabled `automargin: true` on all axes so dynamic label lengths automatically preserve comfortable spacing.

### Locked Non-Zoomable Interaction
On high-frequency operational dashboards, accidental mouse scroll gestures can easily zoom into an arbitrary corner of a chart, throwing axis scales off-screen and disorienting business decision-makers.

**Our Interaction Lock:**
1. **Coordinate Locking:** Applied `fixedrange: true` to all x-axes and y-axes, preventing accidental box zooms and dragging.
2. **Scroll Lock:** Configured Plotly with `scrollZoom: false` to ensure mouse wheel scrolling moves the web page naturally without zooming into graphs.
3. **Double-Click Reset Disabled:** Set `doubleClick: false` and `displayModeBar: false` to eliminate distracting overlay buttons and ensure clean, permanent chart framing.

### Legend Placement
All multi-series charts position their legend horizontally beneath the chart area (`orientation: "h"`, `y: -0.22`), completely preventing legends from obstructing graph titles or line traces.

---

## Part 9 — Git Commit History (What Changed When)

| Commit Hash | Description & Milestone Accomplished |
|:---|:---|
| `4631ef4` | Transition to fully live-data architecture: Auto-connected Square and Stripe feeds, sidebar CSV ingestion, direct live AI nowcasting. |
| `5a9e85b` | Implement dynamic city- and business-specific domino effect engines, fix 1-based table indices, eliminate graph legend overlaps. |
| `24ab5f0` | Update UI branding, labels, and weather intelligence displays across all dashboard tabs. |
| `07bb9c9` | **Milestone: Migrate core platform to standalone web application.** Built Flask REST backend (`server.py`), semantic 5-tab interface (`index.html`), Obsidian Dark styling (`style.css`), and reactive client (`app.js`). Resolved axis label collisions with 85px margins and locked non-zoomable chart coordinates. Safely preserved local Streamlit dashboard files on disk as an operational backup while untracking them from remote Git. |

---

## Part 10 — Summary: What Makes This Project Special

| Analytical Feature | Standard Academic / Student Projects | This Enterprise Platform |
|:---|:---|:---|
| **Application Architecture** | Tied to a single notebook or prototype tool | Full standalone web application (Flask + HTML5/CSS3/JS) plus preserved local backup dashboard |
| **Data Ingestion** | Static, downloaded one-off CSV file | Live multi-source telemetry from 3 real weather APIs plus Square and Stripe payment feeds |
| **Econometric Rigor** | Simple Pearson correlation (confounded by weekends) | Two-Way Fixed Effects panel regressions controlling for city, hour, day, month, and holiday effects |
| **Business Customization** | Single generic chart for the whole dataset | Dynamic calculations customized for 16+ specific business sectors and 5 distinct metropolitan areas |
| **Domino Cascade Modeling** | Generic static descriptive paragraphs | Real-time 6-step causal ripple chain computing exact dollar impacts unique to today's live weather |
| **Predictive Forecasting** | Hypothetical sliders with no external link | 7-day forward financial projections driven by real meteorological numerical weather models |
| **Software Engineering** | Single monolithic script with zero verification | Modular 8-file analytics engine covered by 7 automated tests passing in ~19 seconds |
| **Visual Polish** | Default library styles with label collisions | Obsidian Dark design system, 85px collision-free axis margins, and locked non-zoomable chart geometry |

---

*Project Codebase: `C:\Users\vyasv\.gemini\antigravity\scratch\weather-business-impact-eda`*  
*GitHub Repository: `https://github.com/Vatsal0729/Weather-Driven-Business-Impact-A-Multi-Source-Data-Analysis`*
