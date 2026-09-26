from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.schemas import ProductionRequest, ProductionResponse
from backend.services.production_service import create_demo_batch

router = APIRouter(tags=["Production"])

@router.post("/production", response_model=ProductionResponse, status_code=status.HTTP_201_CREATED)
def create_production_batch(payload: ProductionRequest, db: Session = Depends(get_db)):
    return create_demo_batch(db, payload)
