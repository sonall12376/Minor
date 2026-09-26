import uuid
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Float, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass

class ProductionBatch(Base):
    __tablename__ = "production_batches"
    batch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_name: Mapped[str] = mapped_column(String(100), nullable=False)
    model_version: Mapped[str] = mapped_column(String(50), nullable=False, default="v1.0.0")
    run_timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    record_count: Mapped[int] = mapped_column(Integer, nullable=False)
    execution_time_sec: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    is_drift_detected: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    overall_psi_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    health_score: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    status: Mapped[str] = mapped_column(String(30), nullable=False, default="COMPLETED")
    drift_results: Mapped[list["DriftResult"]] = relationship(back_populates="batch", cascade="all, delete-orphan")

class DriftResult(Base):
    __tablename__ = "drift_results"
    result_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    batch_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("production_batches.batch_id", ondelete="CASCADE"), nullable=False)
    metric_name: Mapped[str] = mapped_column(String(50), nullable=False)
    metric_value: Mapped[float] = mapped_column(Float, nullable=False)
    threshold: Mapped[float] = mapped_column(Float, nullable=False)
    status: Mapped[str] = mapped_column(String(30), nullable=False)
    report_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=datetime.utcnow)
    batch: Mapped["ProductionBatch"] = relationship(back_populates="drift_results")
    feature_drifts: Mapped[list["FeatureDrift"]] = relationship(back_populates="drift_result", cascade="all, delete-orphan")

class FeatureDrift(Base):
    __tablename__ = "feature_drift"
    feature_drift_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    result_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("drift_results.result_id", ondelete="CASCADE"), nullable=False)
    feature_name: Mapped[str] = mapped_column(String(100), nullable=False)
    data_type: Mapped[str] = mapped_column(String(30), nullable=False)
    psi_score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    ks_p_value: Mapped[float | None] = mapped_column(Float, nullable=True)
    drift_status: Mapped[str] = mapped_column(String(30), nullable=False)
    baseline_mean: Mapped[float | None] = mapped_column(Float, nullable=True)
    batch_mean: Mapped[float | None] = mapped_column(Float, nullable=True)
    drift_result: Mapped["DriftResult"] = relationship(back_populates="feature_drifts")
