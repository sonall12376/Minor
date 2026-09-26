CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE IF NOT EXISTS production_batches (
    batch_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_name VARCHAR(100) NOT NULL,
    model_version VARCHAR(50) NOT NULL DEFAULT 'v1.0.0',
    run_timestamp TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    record_count INTEGER NOT NULL CHECK (record_count > 0),
    execution_time_sec DOUBLE PRECISION NOT NULL DEFAULT 0,
    is_drift_detected BOOLEAN NOT NULL DEFAULT FALSE,
    overall_psi_score DOUBLE PRECISION NOT NULL DEFAULT 0,
    health_score DOUBLE PRECISION NOT NULL DEFAULT 100,
    status VARCHAR(30) NOT NULL DEFAULT 'COMPLETED'
);

CREATE TABLE IF NOT EXISTS drift_results (
    result_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    batch_id UUID NOT NULL REFERENCES production_batches(batch_id) ON DELETE CASCADE,
    metric_name VARCHAR(50) NOT NULL,
    metric_value DOUBLE PRECISION NOT NULL,
    threshold DOUBLE PRECISION NOT NULL,
    status VARCHAR(30) NOT NULL,
    report_path TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS feature_drift (
    feature_drift_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    result_id UUID NOT NULL REFERENCES drift_results(result_id) ON DELETE CASCADE,
    feature_name VARCHAR(100) NOT NULL,
    data_type VARCHAR(30) NOT NULL,
    psi_score DOUBLE PRECISION NOT NULL DEFAULT 0,
    ks_p_value DOUBLE PRECISION,
    drift_status VARCHAR(30) NOT NULL,
    baseline_mean DOUBLE PRECISION,
    batch_mean DOUBLE PRECISION
);

CREATE INDEX IF NOT EXISTS idx_production_batches_timestamp ON production_batches(run_timestamp DESC);
CREATE INDEX IF NOT EXISTS idx_drift_results_batch ON drift_results(batch_id);
CREATE INDEX IF NOT EXISTS idx_feature_drift_result ON feature_drift(result_id);
CREATE INDEX IF NOT EXISTS idx_feature_drift_status ON feature_drift(drift_status);
