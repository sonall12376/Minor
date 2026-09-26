from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, Field

class ProductionRequest(BaseModel):
    batch_name: str = "demo_batch"
    model_version: str = "v1.0.0"
    record_count: int = Field(default=100, ge=1)

class ProductionResponse(BaseModel):
    batch_id: UUID
    batch_name: str
    model_version: str
    record_count: int
    is_drift_detected: bool
    overall_psi_score: float
    health_score: float
    status: str
    run_timestamp: datetime
    model_config = {"from_attributes": True}

class FeatureDriftResponse(BaseModel):
    feature_name: str
    data_type: str
    psi_score: float
    ks_p_value: float | None
    drift_status: str
    baseline_mean: float | None
    batch_mean: float | None
    model_config = {"from_attributes": True}

class DriftResponse(BaseModel):
    batch_id: UUID
    overall_psi_score: float
    is_drift_detected: bool
    health_score: float
    features: list[FeatureDriftResponse]

class HistoryItem(BaseModel):
    batch_id: UUID
    batch_name: str
    model_version: str
    run_timestamp: datetime
    record_count: int
    overall_psi_score: float
    is_drift_detected: bool
    health_score: float
    status: str
    model_config = {"from_attributes": True}
