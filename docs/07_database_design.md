# Database Design Document

**Project Title:** An Automated MLOps Framework for Monitoring and Diagnosing Model Degradation in Production  
**Document Version:** 1.0.0  
**Status:** Approved / Draft  
**Target Database:** Supabase (Cloud PostgreSQL 15+)  
**ORM Layer:** SQLAlchemy 2.0  
**Date:** September 2026  

---

## 1. Architectural Overview & Storage Strategy

The persistence layer relies on **Supabase Cloud PostgreSQL** accessed via **SQLAlchemy 2.0 ORM** and the `psycopg2-binary` driver. 

### 1.1 Core Objectives
- Store baseline model metadata, training metrics, and reference feature distributions.
- Persist batch monitoring execution runs, execution duration, and global drift flags.
- Record fine-grained feature-level statistical drift scores (PSI, K-S $p$-values, Chi-Square $p$-values).
- Track post-deployment confusion matrices and accuracy degradation.
- Log SHAP feature attribution shifts to support root-cause analysis.
- Maintain an audit log of automated system drift alerts.

---

## 2. Entity-Relationship (ER) Diagram

```mermaid
erdiagram
    MODEL_VERSIONS ||--o{ BATCH_RUNS : "evaluates"
    BATCH_RUNS ||--o{ FEATURE_DRIFT_LOGS : "contains"
    BATCH_RUNS ||--o{ MODEL_PERFORMANCE_LOGS : "records"
    BATCH_RUNS ||--o{ SHAP_IMPORTANCE_LOGS : "diagnoses"
    BATCH_RUNS ||--o{ ALERT_LOGS : "triggers"

    MODEL_VERSIONS {
        uuid model_id PK
        string version_name
        string algorithm_name
        timestamp trained_at
        jsonb training_metrics
        string baseline_json_path
        boolean is_active
    }

    BATCH_RUNS {
        uuid batch_id PK
        uuid model_id FK
        timestamp run_timestamp
        int record_count
        float execution_time_sec
        boolean is_drift_detected
        float overall_psi_score
        string status
    }

    FEATURE_DRIFT_LOGS {
        uuid log_id PK
        uuid batch_id FK
        string feature_name
        string data_type
        float psi_score
        float ks_p_value
        float chi_square_p_value
        string drift_status
        float baseline_mean
        float batch_mean
    }

    MODEL_PERFORMANCE_LOGS {
        uuid perf_id PK
        uuid batch_id FK
        float accuracy
        float precision
        float recall
        float f1_score
        float roc_auc
        jsonb confusion_matrix
    }

    SHAP_IMPORTANCE_LOGS {
        uuid shap_id PK
        uuid batch_id FK
        string feature_name
        float baseline_mean_shap
        float batch_mean_shap
        int rank_shift
    }

    ALERT_LOGS {
        uuid alert_id PK
        uuid batch_id FK
        string alert_level
        string alert_type
        text message
        boolean is_resolved
        timestamp created_at
    }
```

---

## 3. Detailed Data Dictionary & SQL Schema DDL

Below are the complete, production-ready PostgreSQL DDL statements for creating the monitoring database in Supabase.

```sql
-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Table 1: MODEL_VERSIONS
CREATE TABLE model_versions (
    model_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    version_name VARCHAR(50) NOT NULL UNIQUE,
    algorithm_name VARCHAR(100) NOT NULL,
    trained_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    training_metrics JSONB NOT NULL,
    baseline_json_path VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT TRUE
);

-- Table 2: BATCH_RUNS
CREATE TABLE batch_runs (
    batch_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    model_id UUID NOT NULL REFERENCES model_versions(model_id) ON DELETE CASCADE,
    run_timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    record_count INT NOT NULL CHECK (record_count > 0),
    execution_time_sec FLOAT NOT NULL,
    is_drift_detected BOOLEAN NOT NULL DEFAULT FALSE,
    overall_psi_score FLOAT NOT NULL,
    status VARCHAR(30) NOT NULL DEFAULT 'COMPLETED'
);

-- Table 3: FEATURE_DRIFT_LOGS
CREATE TABLE feature_drift_logs (
    log_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_id UUID NOT NULL REFERENCES batch_runs(batch_id) ON DELETE CASCADE,
    feature_name VARCHAR(100) NOT NULL,
    data_type VARCHAR(30) NOT NULL,
    psi_score FLOAT NOT NULL,
    ks_p_value FLOAT,
    chi_square_p_value FLOAT,
    drift_status VARCHAR(30) NOT NULL, -- 'NO_DRIFT', 'MODERATE_DRIFT', 'CRITICAL_DRIFT'
    baseline_mean FLOAT,
    batch_mean FLOAT
);

-- Table 4: MODEL_PERFORMANCE_LOGS
CREATE TABLE model_performance_logs (
    perf_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_id UUID NOT NULL REFERENCES batch_runs(batch_id) ON DELETE CASCADE,
    accuracy FLOAT NOT NULL,
    precision FLOAT NOT NULL,
    recall FLOAT NOT NULL,
    f1_score FLOAT NOT NULL,
    roc_auc FLOAT NOT NULL,
    confusion_matrix JSONB NOT NULL
);

-- Table 5: SHAP_IMPORTANCE_LOGS
CREATE TABLE shap_importance_logs (
    shap_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_id UUID NOT NULL REFERENCES batch_runs(batch_id) ON DELETE CASCADE,
    feature_name VARCHAR(100) NOT NULL,
    baseline_mean_shap FLOAT NOT NULL,
    batch_mean_shap FLOAT NOT NULL,
    rank_shift INT NOT NULL
);

-- Table 6: ALERT_LOGS
CREATE TABLE alert_logs (
    alert_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_id UUID NOT NULL REFERENCES batch_runs(batch_id) ON DELETE CASCADE,
    alert_level VARCHAR(20) NOT NULL, -- 'INFO', 'WARNING', 'CRITICAL'
    alert_type VARCHAR(50) NOT NULL,  -- 'FEATURE_DRIFT', 'PERFORMANCE_DECAY'
    message TEXT NOT NULL,
    is_resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

---

## 4. Indexing & Query Optimization Strategy

To ensure sub-second rendering of Streamlit dashboard charts and rapid FastAPI lookups, targeted indexes are applied to foreign keys and filtering columns:

```sql
-- Indexes for batch query filtering
CREATE INDEX idx_batch_runs_timestamp ON batch_runs(run_timestamp DESC);
CREATE INDEX idx_batch_runs_model ON batch_runs(model_id);

-- Indexes for feature drift analytics
CREATE INDEX idx_feature_drift_batch ON feature_drift_logs(batch_id);
CREATE INDEX idx_feature_drift_status ON feature_drift_logs(drift_status);
CREATE INDEX idx_feature_drift_feature ON feature_drift_logs(feature_name);

-- Indexes for SHAP diagnostics & alerts
CREATE INDEX idx_shap_logs_batch ON shap_importance_logs(batch_id);
CREATE INDEX idx_alerts_batch ON alert_logs(batch_id);
CREATE INDEX idx_alerts_unresolved ON alert_logs(is_resolved) WHERE is_resolved = FALSE;
```

---

## 5. SQLAlchemy 2.0 ORM Declarative Models (`src/database/models.py`)

```python
import uuid
from datetime import datetime
from typing import List, Optional
from sqlalchemy import String, Float, Integer, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Base(DeclarativeBase):
    pass

class ModelVersion(Base):
    __tablename__ = "model_versions"

    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    version_name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    algorithm_name: Mapped[str] = mapped_column(String(100), nullable=False)
    trained_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    training_metrics: Mapped[dict] = mapped_column(JSONB, nullable=False)
    baseline_json_path: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    batch_runs: Mapped[List["BatchRun"]] = relationship("BatchRun", back_populates="model_version", cascade="all, delete-orphan")

class BatchRun(Base):
    __tablename__ = "batch_runs"

    batch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    model_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("model_versions.model_id", ondelete="CASCADE"), nullable=False)
    run_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    record_count: Mapped[int] = mapped_column(Integer, nullable=False)
    execution_time_sec: Mapped[float] = mapped_column(Float, nullable=False)
    is_drift_detected: Mapped[bool] = mapped_column(Boolean, default=False)
    overall_psi_score: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(30), default="COMPLETED")

    model_version: Mapped["ModelVersion"] = relationship("ModelVersion", back_populates="batch_runs")
    feature_drifts: Mapped[List["FeatureDriftLog"]] = relationship("FeatureDriftLog", back_populates="batch_run", cascade="all, delete-orphan")
    performance_logs: Mapped[List["ModelPerformanceLog"]] = relationship("ModelPerformanceLog", back_populates="batch_run", cascade="all, delete-orphan")
    shap_logs: Mapped[List["ShapImportanceLog"]] = relationship("ShapImportanceLog", back_populates="batch_run", cascade="all, delete-orphan")
    alerts: Mapped[List["AlertLog"]] = relationship("AlertLog", back_populates="batch_run", cascade="all, delete-orphan")

class FeatureDriftLog(Base):
    __tablename__ = "feature_drift_logs"

    log_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("batch_runs.batch_id", ondelete="CASCADE"), nullable=False)
    feature_name: Mapped[str] = mapped_column(String(100), nullable=False)
    data_type: Mapped[str] = mapped_column(String(30), nullable=False)
    psi_score: Mapped[float] = mapped_column(Float, nullable=False)
    ks_p_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    chi_square_p_value: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    drift_status: Mapped[str] = mapped_column(String(30), nullable=False)
    baseline_mean: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    batch_mean: Mapped[Optional[float]] = mapped_column(Float, nullable=True)

    batch_run: Mapped["BatchRun"] = relationship("BatchRun", back_populates="feature_drifts")
```

---

## 6. Database Connection Pooling Configuration

To manage connection overhead to Supabase Cloud PostgreSQL, `src/database/connection.py` configures engine connection pooling:

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.utils.config import settings

engine = create_engine(
    settings.SUPABASE_DB_URL,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800,
    pool_pre_ping=True,  # Automatically detects closed cloud connections
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
```

---

## 7. Document Approval & Sign-Off

- **Prepared By:** Lead Database & Backend Engineer (Developer 2)  
- **Reviewed By:** Senior MLOps Solution Architect & Developer 1  
- **Status:** Approved for Schema Deployment  

---
