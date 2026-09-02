# Data Flow Document

**Project Title:** An Automated MLOps Framework for Monitoring and Diagnosing Model Degradation in Production  
**Document Version:** 1.0.0  
**Status:** Approved / Draft  
**Target Audience:** Data Engineers, ML Engineers, Backend Developers, System Architects  
**Date:** September 2026  

---

## 1. Architectural Overview & Data Lifecycle

The framework ingests normalized multi-table CSV files representing SaaS customer entities, transforms them into single-row-per-account feature vectors, evaluates model predictions, computes statistical distribution shifts against an offline baseline profile, calculates SHAP feature attributions, and persists all diagnostic logs into Supabase PostgreSQL.

```mermaid
flowchart TD
    subgraph Stage1["1. Multi-Table Ingestion"]
        A1[accounts.csv]
        A2[subscriptions.csv]
        A3[feature_usage.csv]
        A4[support_tickets.csv]
    end

    subgraph Stage2["2. Relational Transformation"]
        FK[Relational Joiner: Foreign Key Join on account_id]
        FA[Feature Aggregator: Windowing & Summary Stats]
    end

    subgraph Stage3["3. Inference & Baselining"]
        INF[Scikit-learn Model Inference]
        REF[Load Baseline Reference JSON Profile]
    end

    subgraph Stage4["4. Statistical Drift Suite"]
        PSI[PSI Calculator]
        KS[K-S Continuous Test]
        CHI[Chi-Square Categorical Test]
        EVI[Evidently AI Summary Generator]
    end

    subgraph Stage5["5. SHAP Diagnosis"]
        SHAP[SHAP TreeExplainer Engine]
    end

    subgraph Stage6["6. Persistence & UI"]
        DB[(Supabase PostgreSQL Database)]
        UI[Streamlit Operations UI Dashboard]
    end

    A1 & A2 & A3 & A4 --> FK
    FK --> FA
    FA --> INF & REF
    INF & REF --> PSI & KS & CHI & EVI
    INF --> SHAP
    PSI & KS & CHI & EVI & SHAP --> DB
    DB <--> UI
```

---

## 2. Data Flow Diagrams (DFD)

### 2.1 DFD Level 0: High-Level Context Diagram

```mermaid
flowchart LR
    User[MLOps Operator / System] -->|Upload Batch Relational CSVs| System((MLOps Monitoring Framework))
    System -->|Render Plotly Charts & Alerts| User
    System <-->|Read / Write Drift Logs| Supabase[(Supabase Cloud Database)]
```

### 2.2 DFD Level 1: Detailed System Processing Flow

```mermaid
flowchart TD
    P1[1.0 Ingest CSV Files] -->|Raw DataFrames| P2[2.0 Execute Relational Merges]
    P2 -->|Merged Account DF| P3[3.0 Aggregate Features]
    P3 -->|Feature Matrix| P4[4.0 Execute Model Predictions]
    P3 & P4 -->|Production Batch Data| P5[5.0 Calculate Statistical Drift]
    P3 & P4 -->|Batch Predictions| P6[6.0 Compute SHAP Attributions]
    P5 & P6 -->|Drift Scores & SHAP Values| P7[7.0 Persist Metrics to Supabase]
    P7 -->|SQLAlchemy Sessions| DB[(Supabase Database)]
    DB -->|ORM Queries| P8[8.0 Render Streamlit Visualizations]
```

---

## 3. Data Transformation & Schema Lineage

Below is the field-level data lineage table tracking how raw multi-table RavenStack CSV columns transform into model features, statistical metrics, and database log columns.

| Raw Source Table | Raw Input Column | Transformation / Aggregation Rule | Target Feature Name | Feature Type | Target Database Column |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `accounts` | `company_size` | Categorical encoding (Small, Mid, Enterprise) | `company_size_code` | Categorical | `feature_drift_logs.feature_name` |
| `accounts` | `signup_date` | Days since signup = $\text{Today} - \text{signup\_date}$ | `account_tenure_days` | Numerical | `feature_drift_logs.feature_name` |
| `subscriptions` | `monthly_recurring_revenue` | Direct floating-point extraction | `mrr` | Continuous | `feature_drift_logs.feature_name` |
| `subscriptions` | `billing_frequency` | One-hot / Label encoding (Monthly, Annual) | `is_annual_billing` | Categorical | `feature_drift_logs.feature_name` |
| `feature_usage` | `api_call_count` | Sum over last 30 days per `account_id` | `total_api_calls_30d` | Continuous | `feature_drift_logs.feature_name` |
| `feature_usage` | `daily_active_users` | Mean DAU per `account_id` over 30 days | `mean_dau_30d` | Continuous | `feature_drift_logs.feature_name` |
| `support_tickets` | `resolution_time_hours` | Mean resolution hours per `account_id` | `avg_ticket_resolution_hours` | Continuous | `feature_drift_logs.feature_name` |
| `support_tickets` | `ticket_id` | Count of tickets per `account_id` | `total_support_tickets` | Continuous | `feature_drift_logs.feature_name` |
| `churn_labels` | `is_churned` | Target ground truth label ($0$ or $1$) | `is_churned` | Binary Target | `model_performance_logs.f1_score` |

---

## 4. Statistical Drift Computation Flow

```mermaid
flowchart TD
    Start[Production Batch Matrix + Baseline Profile JSON] --> CheckType{Feature Type?}
    
    CheckType -- Numerical / Continuous --> PSI_Proc[Run PSI Binned Ratio Calculation]
    PSI_Proc --> KS_Proc[Run scipy.stats.ks_2samp Test]
    KS_Proc --> Eval_Num{PSI >= 0.25 OR p-val < 0.05?}
    
    CheckType -- Categorical --> CHI_Proc[Run scipy.stats.chisquare Test]
    CHI_Proc --> Eval_Cat{p-val < 0.05?}
    
    Eval_Num -- Yes --> Flag_Crit[Set status = CRITICAL_DRIFT]
    Eval_Num -- No --> Flag_OK[Set status = NO_DRIFT]
    
    Eval_Cat -- Yes --> Flag_Crit
    Eval_Cat -- No --> Flag_OK
    
    Flag_Crit & Flag_OK --> Aggregate[Aggregate Overall Batch PSI & Trigger Alerts]
```

---

## 5. Data Quality & Error Guardrails

To prevent pipeline crashes during automated batch runs, data validation guardrails are enforced at each transition stage:

1. **Primary Key Alignment Guardrail:** If an `account_id` in `subscriptions` or `feature_usage` does not exist in `accounts`, the row is isolated in an orphan queue and logged without halting the join.
2. **Missing Value Imputation:**
   - Numerical feature missing values (e.g., accounts with zero support tickets) are imputed with explicit zero values (`0.0`).
   - Categorical missing values are filled with `'UNKNOWN'`.
3. **Zero Variance Guardrail:** If a continuous feature in a production batch has zero variance ($\sigma = 0$), K-S testing is skipped, and a default non-drift warning flag is recorded to prevent division-by-zero runtime exceptions.
4. **Minimum Batch Sample Size Enforcement:** A minimum threshold of $N \ge 100$ records is required before executing K-S and Chi-Square statistical tests to avoid sample size bias false positives.

---

## 6. Document Approval & Sign-Off

- **Prepared By:** Senior Data Engineer & MLOps Architect  
- **Reviewed By:** Lead Data Scientist & Backend Lead  
- **Status:** Approved for Pipeline Implementation  

---
