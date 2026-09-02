# An Automated MLOps Framework for Monitoring and Diagnosing Model Degradation in Production

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/FastAPI-0.104.1-green.svg)](https://fastapi.tiangolo.com/)
[![Dashboard](https://img.shields.io/badge/Streamlit-1.28.0-red.svg)](https://streamlit.io/)
[![Database](https://img.shields.io/badge/Supabase-PostgreSQL-emerald.svg)](https://supabase.com/)
[![ML Engine](https://img.shields.io/badge/Scikit--Learn-1.3.2-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-lightgrey.svg)](LICENSE)

---

## 1. Project Overview

In enterprise SaaS platforms, machine learning models predicting customer churn inevitably degrade over time due to **Data Drift** (shifting input feature distributions) and **Concept Drift** (evolving customer behavior). 

This project delivers an **Automated MLOps Monitoring and Diagnostic Framework** designed to evaluate production batch data, detect statistical distribution shifts, diagnose root-cause feature degradation using **SHAP**, persist audit logs into **Supabase Cloud PostgreSQL**, and visualize monitoring operations through an interactive **Streamlit** dashboard.

The framework natively ingests the multi-table relational **RavenStack Synthetic SaaS Dataset**, preserving relational database integrity (`accounts`, `subscriptions`, `feature_usage`, `support_tickets`) rather than oversimplifying data into a flat CSV.

---

## 2. Key Architecture Capabilities

- **Relational Data Processing Pipeline:** Merges multi-table RavenStack CSVs on `account_id` and aggregates windowed usage metrics.
- **Statistical Drift Detection Suite:**
  - **Population Stability Index (PSI):** Measures overall continuous feature distribution shifts.
  - **Kolmogorov-Smirnov (K-S) Test:** Non-parametric continuous distribution drift detection ($p < 0.05$).
  - **Chi-Square ($\chi^2$) Test:** Categorical feature frequency shift detection.
  - **Evidently AI Integration:** Automatically generates comprehensive HTML/JSON Data Drift & Quality reports.
- **Explainable Failure Diagnosis (SHAP):** Leverages `shap.TreeExplainer` to attribute post-deployment prediction changes to specific feature importance rank shifts.
- **Cloud Persistence & ORM:** Persists batch runs, feature drift scores, performance metrics, and alerts into **Supabase PostgreSQL** via **SQLAlchemy 2.0**.
- **RESTful API Backend:** High-speed **FastAPI** endpoints powering execution requests and metric queries.
- **Operations Dashboard:** Multi-page **Streamlit** application rendering interactive **Plotly** charts and generating PDF/HTML drift reports.

---

## 3. High-Level Architecture Diagram

```mermaid
flowchart LR
    subgraph Ingestion["Data Layer"]
        CSV[RavenStack Relational CSVs]
    end

    subgraph Core["MLOps Diagnostic Core"]
        Join[Relational Ingestion Engine]
        ML[Scikit-learn Model]
        Drift[PSI / KS / Chi2 / Evidently]
        SHAP[SHAP TreeExplainer Engine]
    end

    subgraph Backend["Backend & DB Layer"]
        API[FastAPI REST API]
        DB[(Supabase PostgreSQL)]
    end

    subgraph Frontend["Operations UI"]
        UI[Streamlit Dashboard & Plotly]
    end

    CSV --> Join
    Join --> ML
    ML --> Drift & SHAP
    Drift & SHAP --> API
    API <-->|SQLAlchemy ORM| DB
    API <-->|JSON Payloads| UI
```

---

## 4. Repository Directory Structure

```text
Minor/
├── docs/                   # Complete architectural documentation (01 to 17)
├── data/
│   ├── raw/                # Raw RavenStack multi-table CSVs
│   ├── processed/          # Aggregated feature matrices
│   └── baseline/           # Baseline reference profile JSON
├── models/                 # Serialized Scikit-learn models & scalers
├── src/
│   ├── ingestion/          # Relational joiner & feature aggregator
│   ├── ml_engine/           # Scikit-learn trainer & baseline builder
│   ├── drift_engine/       # PSI, KS, Chi-Square & Evidently runners
│   ├── explainability/     # SHAP TreeExplainer attribution engine
│   ├── database/           # SQLAlchemy ORM models & Supabase connection
│   ├── api/                # FastAPI application endpoints & routers
│   ├── dashboard/          # Streamlit multi-page UI app & Plotly charts
│   └── utils/              # Configuration & logger helpers
├── tests/                  # Unit and integration Pytest suites
├── requirements.txt        # Python dependency versions
├── run_api.py              # FastAPI server launcher
└── run_dashboard.py        # Streamlit dashboard launcher
```

---

## 5. Local Setup & Installation Guide

### 5.1 Prerequisites
- **Python:** Version `3.10.x` or higher installed.
- **Git:** Version control installed.
- **Supabase Account:** Free-tier Cloud PostgreSQL instance provisioned.

### 5.2 Environment Setup
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/your-username/Minor.git
   cd Minor
   ```

2. **Create and Activate Virtual Environment:**
   - **Windows:**
     ```bash
     python -m venv venv
     .\venv\Scripts\activate
     ```
   - **Linux / macOS:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Copy `.env.example` to create your local `.env` file:
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and fill in your Supabase database credentials:
   ```env
   SUPABASE_DB_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   API_HOST=127.0.0.1
   API_PORT=8000
   LOG_LEVEL=INFO
   ```

---

## 6. Running the Application

### 6.1 Step 1: Start FastAPI REST Backend
In terminal window 1, launch the FastAPI server:
```bash
python run_api.py
```
- API Base URL: `http://localhost:8000/api/v1`
- Interactive OpenAPI Swagger Docs: `http://localhost:8000/docs`

### 6.2 Step 2: Start Streamlit Operations UI
In terminal window 2, launch the Streamlit dashboard:
```bash
python run_dashboard.py
```
- Streamlit UI Dashboard: `http://localhost:8501`

---

## 7. Running Tests

Execute the automated test suite using `pytest`:

```bash
# Run all unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/

# Run test suite with coverage report
pytest --cov=src tests/
```

---

## 8. Team & Responsibilities

- **Developer 1 (Data Science & ML Engineer):** Data Ingestion, Relational Aggregation, Scikit-learn Model Training, Baseline JSON Generation, Drift Detection Engine (PSI, K-S, Chi2, Evidently), and SHAP Diagnosis.
- **Developer 2 (Backend & MLOps Engineer):** FastAPI Backend REST API, Supabase Cloud PostgreSQL Database, SQLAlchemy ORM Models, Streamlit UI Operations Dashboard, Plotly Charts, and CI/CD Setup.

---

## 9. License

This project is licensed under the MIT License - see the `LICENSE` file for details.

---
