# File Specification Document

**Project Title:** An Automated MLOps Framework for Monitoring and Diagnosing Model Degradation in Production  
**Document Version:** 1.0.0  
**Status:** Approved / Draft  
**Target Audience:** All Engineering Team Members, Technical Reviewers  
**Date:** September 2026  

---

## 1. Executive Summary

This document provides a granular file-by-file specification of every source code, configuration, dataset, artifact, and test file in the repository. It details file paths, primary ownership (Developer 1 vs Developer 2), functional responsibilities, inputs, and outputs.

---

## 2. Comprehensive File Inventory & Specification Matrix

### 2.1 Root Execution & Environment Configuration Files

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs / Side Effects |
| :--- | :--- | :--- | :--- | :--- |
| `run_api.py` | Developer 2 | Entry point script executing Uvicorn ASGI server hosting FastAPI. | Command line args, `.env` | Starts API server on port 8000. |
| `run_dashboard.py` | Developer 2 | Entry point launching multi-page Streamlit dashboard server. | Command line args | Renders UI on port 8501. |
| `requirements.txt` | Dev 1 & Dev 2 | Pinning exact library versions for Python environment reproducibility. | N/A | Dependency installation source. |
| `.env.example` | Developer 2 | Template for required system environment variables (DB URLs, keys). | N/A | Guides local `.env` creation. |
| `.gitignore` | Developer 2 | Prevents tracking of virtual environments, `.env` secrets, and raw data. | N/A | Git file exclusion rules. |

---

### 2.2 Data Ingestion Subsystem (`src/ingestion/`)

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `src/ingestion/__init__.py` | Developer 1 | Package initialization exposing public ingestion classes. | N/A | Module namespace. |
| `src/ingestion/csv_loader.py` | Developer 1 | Ingests raw multi-table RavenStack CSVs from disk or UploadFile handlers. | CSV file paths / binary streams | Dictionary of Pandas DataFrames. |
| `src/ingestion/relational_joiner.py` | Developer 1 | Merges relational tables on `account_id` using left outer joins. | Raw DataFrames dict | Single joined DataFrame. |
| `src/ingestion/feature_aggregator.py` | Developer 1 | Computes windowed summary statistics per `account_id`. | Joined DataFrame | Processed Feature Matrix DataFrame. |
| `src/ingestion/schema_validator.py` | Developer 1 | Validates data types, missing required columns, and schema rules. | Feature Matrix DataFrame | Validated DataFrame or Raises Error. |

---

### 2.3 Machine Learning Engine (`src/ml_engine/`)

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `src/ml_engine/trainer.py` | Developer 1 | Trains Scikit-learn binary classification model on reference data. | Processed Feature Matrix | `models/churn_model.pkl`. |
| `src/ml_engine/evaluator.py` | Developer 1 | Computes baseline confusion matrix, F1, ROC-AUC, Precision, and Recall. | Model, Test Feature Matrix | Evaluation metrics dict. |
| `src/ml_engine/baseline_builder.py` | Developer 1 | Extracts feature distributions, bin edges, means, stds from training data. | Training Feature Matrix | `data/baseline/baseline_reference.json`. |
| `src/ml_engine/predictor.py` | Developer 1 | Loads serialized model artifact and executes batch probability predictions. | `churn_model.pkl`, Batch DF | Probability array & class predictions. |

---

### 2.4 Statistical Drift Detection Engine (`src/drift_engine/`)

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `src/drift_engine/psi_calculator.py` | Developer 1 | Calculates Population Stability Index for continuous numerical features. | Baseline Series, Batch Series | PSI float score per feature. |
| `src/drift_engine/ks_tester.py` | Developer 1 | Runs scipy.stats.ks_2samp continuous non-parametric test. | Baseline Series, Batch Series | Dict containing `ks_stat` and `p_value`. |
| `src/drift_engine/chi_square_tester.py` | Developer 1 | Runs scipy.stats.chisquare test on categorical feature distributions. | Baseline Series, Batch Series | Dict containing `chi2_stat` and `p_value`. |
| `src/drift_engine/evidently_runner.py` | Developer 1 | Wraps Evidently AI to generate HTML/JSON Data Drift & Quality reports. | Reference DF, Production DF | Evidently HTML string / JSON dict. |
| `src/drift_engine/drift_evaluator.py` | Developer 1 | Orchestrates all drift tests into a unified batch evaluation dictionary. | Baseline JSON, Production DF | Comprehensive Batch Drift Dict. |

---

### 2.5 Explainability Subsystem (`src/explainability/`)

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `src/explainability/shap_explainer.py` | Developer 1 | Computes SHAP value matrices using `shap.TreeExplainer`. | Model, Production Batch DF | Matrix of SHAP values. |
| `src/explainability/root_cause_analyzer.py` | Developer 1 | Compares baseline vs production mean absolute SHAP values and rank shifts. | Baseline SHAP, Batch SHAP | Ranked feature importance shift list. |

---

### 2.6 Persistence Layer (`src/database/`)

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `src/database/connection.py` | Developer 2 | Configures SQLAlchemy engine connection pool to Supabase PostgreSQL. | `SUPABASE_DB_URL` env | SQLAlchemy `engine` & `SessionLocal`. |
| `src/database/models.py` | Developer 2 | Declarative ORM models (`ModelVersion`, `BatchRun`, `FeatureDriftLog`, `AlertLog`). | SQLAlchemy Base | PostgreSQL tables mapping. |
| `src/database/schemas.py` | Developer 2 | Pydantic request and response validation schemas for API serialization. | Pydantic BaseModel | Strongly typed JSON schemas. |
| `src/database/repository.py` | Developer 2 | Encapsulates CRUD functions for creating and querying monitoring logs. | DB Session, Pydantic objects | Persisted ORM database records. |

---

### 2.7 REST API Layer (`src/api/`)

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `src/api/app.py` | Developer 2 | Initializes FastAPI application instance, CORS middleware, and router inclusions. | FastAPI Config | Running FastAPI application instance. |
| `src/api/dependencies.py` | Developer 2 | Dependency injection providers (DB session context manager, API keys). | Request Header / Context | Injected DB session / service instances. |
| `src/api/routers/monitoring.py` | Developer 2 | Router for POST `/run-batch` and GET `/monitoring/history` endpoints. | HTTP Payloads / CSV files | JSON responses (`BatchRunResponse`). |
| `src/api/routers/drift.py` | Developer 2 | Router for GET `/drift/summary` and GET `/drift/features` endpoints. | `batch_id` UUID | JSON feature drift details. |
| `src/api/routers/explainability.py` | Developer 2 | Router for GET `/explainability/shap-summary` endpoint. | `batch_id` UUID | JSON SHAP attribution breakdown. |

---

### 2.8 Streamlit Dashboard UI (`src/dashboard/`)

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `src/dashboard/app.py` | Developer 2 | Main Streamlit navigation layout and global sidebar styling. | User UI Interactions | Streamlit multi-page dashboard app. |
| `src/dashboard/components/drift_charts.py` | Developer 2 | Plotly chart builders for feature distribution overlays & PSI bar charts. | Drift JSON data | Plotly Figure objects. |
| `src/dashboard/components/shap_plots.py` | Developer 2 | Plotly bar charts depicting global SHAP feature importance rank shifts. | SHAP JSON data | Plotly Figure objects. |
| `src/dashboard/pages/1_Overview.py` | Developer 2 | Streamlit page: System status KPI cards, active drift alerts, summary stats. | API Endpoints | Interactive UI page. |
| `src/dashboard/pages/2_Drift_Analysis.py` | Developer 2 | Streamlit page: Per-feature statistical distribution drift drill-downs. | API Endpoints | Interactive UI page. |
| `src/dashboard/pages/3_SHAP_Diagnosis.py` | Developer 2 | Streamlit page: Root-cause diagnosis breakdown using SHAP feature shifts. | API Endpoints | Interactive UI page. |
| `src/dashboard/pages/4_Historical_Logs.py` | Developer 2 | Streamlit page: Query and filter historical batch run logs from Supabase. | API Endpoints | Interactive UI page. |

---

### 2.9 Test Suite (`tests/`)

| File Path | Lead Owner | Primary Responsibility | Inputs | Outputs |
| :--- | :--- | :--- | :--- | :--- |
| `tests/conftest.py` | Dev 1 & Dev 2 | Pytest fixtures providing synthetic DataFrames, mock DB sessions, and API clients. | Pytest context | Reusable test fixtures. |
| `tests/unit/test_ingestion.py` | Developer 1 | Unit tests for relational joiner, aggregator, and schema validator. | Mock RavenStack CSVs | Test assertion results. |
| `tests/unit/test_drift_engine.py` | Developer 1 | Unit tests verifying mathematical accuracy of PSI, K-S test, and Chi-Square. | Synthetic drift Series | Test assertion results. |
| `tests/unit/test_explainability.py` | Developer 1 | Unit tests verifying SHAP calculation and rank shift logic. | Scikit-learn model, batch | Test assertion results. |
| `tests/unit/test_database.py` | Developer 2 | Unit tests for SQLAlchemy ORM models, session context, and CRUD queries. | Test SQLite/Postgres DB | Test assertion results. |
| `tests/integration/test_api_endpoints.py` | Developer 2 | Integration tests querying FastAPI endpoints via `TestClient`. | HTTP Requests | Test assertion results. |
| `tests/integration/test_end_to_end_pipeline.py` | Dev 1 & Dev 2 | Complete pipeline integration test from raw CSV upload to UI response. | Raw RavenStack CSVs | Test assertion results. |

---

## 3. Document Approval & Sign-Off

- **Prepared By:** Senior Technical Lead & Solutions Architect  
- **Reviewed By:** Data Science Lead (Dev 1) & Backend Lead (Dev 2)  
- **Status:** Approved for Codebase Implementation  

---
