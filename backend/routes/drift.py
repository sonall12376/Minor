from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import ProductionBatch, DriftResult
from backend.schemas import DriftResponse, FeatureDriftResponse

router = APIRouter(tags=["Drift"])

def build_response(batch, result):
    features = [FeatureDriftResponse.model_validate(x) for x in (result.feature_drifts if result else [])]
    return DriftResponse(
        batch_id=batch.batch_id,
        overall_psi_score=batch.overall_psi_score,
        is_drift_detected=batch.is_drift_detected,
        health_score=batch.health_score,
        features=features,
    )

@router.get("/drift", response_model=DriftResponse)
def get_latest_drift(db: Session = Depends(get_db)):
    batch = db.query(ProductionBatch).order_by(ProductionBatch.run_timestamp.desc()).first()
    if batch is None:
        raise HTTPException(status_code=404, detail="No production batch found.")
    result = db.query(DriftResult).filter(DriftResult.batch_id == batch.batch_id).first()
    return build_response(batch, result)

@router.get("/drift/{batch_id}", response_model=DriftResponse)
def get_batch_drift(batch_id: UUID, db: Session = Depends(get_db)):
    batch = db.get(ProductionBatch, batch_id)
    if batch is None:
        raise HTTPException(status_code=404, detail="Batch not found.")
    result = db.query(DriftResult).filter(DriftResult.batch_id == batch_id).first()
    return build_response(batch, result)
