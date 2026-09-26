from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models import ProductionBatch
from backend.schemas import HistoryItem

router = APIRouter(tags=["History"])

@router.get("/history", response_model=list[HistoryItem])
def get_history(limit: int = 20, db: Session = Depends(get_db)):
    limit = min(max(limit, 1), 100)
    return db.query(ProductionBatch).order_by(ProductionBatch.run_timestamp.desc()).limit(limit).all()
