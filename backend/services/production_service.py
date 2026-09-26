from sqlalchemy.orm import Session
from backend.models import ProductionBatch, DriftResult, FeatureDrift
from backend.schemas import ProductionRequest

def create_demo_batch(db: Session, payload: ProductionRequest):
    # Temporary mid-term placeholder. Replace with actual ML pipeline output.
    batch = ProductionBatch(
        batch_name=payload.batch_name,
        model_version=payload.model_version,
        record_count=payload.record_count,
        execution_time_sec=0.42,
        is_drift_detected=True,
        overall_psi_score=0.285,
        health_score=71.5,
        status="COMPLETED",
    )
    db.add(batch)
    db.flush()

    result = DriftResult(
        batch_id=batch.batch_id,
        metric_name="PSI",
        metric_value=0.285,
        threshold=0.25,
        status="DRIFT_DETECTED",
        report_path="reports/evidently/demo_report.html",
    )
    db.add(result)
    db.flush()

    db.add_all([
        FeatureDrift(
            result_id=result.result_id, feature_name="monthly_recurring_revenue",
            data_type="continuous", psi_score=0.041, ks_p_value=0.621,
            drift_status="NO_DRIFT", baseline_mean=250.0, batch_mean=248.5,
        ),
        FeatureDrift(
            result_id=result.result_id, feature_name="avg_ticket_resolution_hours",
            data_type="continuous", psi_score=0.342, ks_p_value=0.0004,
            drift_status="CRITICAL_DRIFT", baseline_mean=12.4, batch_mean=28.7,
        ),
    ])
    db.commit()
    db.refresh(batch)
    return batch
