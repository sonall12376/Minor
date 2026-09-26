from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.config import settings
from backend.database import check_database, engine
from backend.models import Base
from backend.routes.production import router as production_router
from backend.routes.drift import router as drift_router
from backend.routes.history import router as history_router

app = FastAPI(title=settings.app_name, version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if settings.cors_origins == "*" else settings.cors_origins.split(","),
    allow_credentials=True, allow_methods=["*"], allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    if engine is not None:
        Base.metadata.create_all(bind=engine)

@app.get("/health")
def health():
    db_ok = check_database()
    return {
        "status": "healthy" if db_ok else "degraded",
        "database": "connected" if db_ok else "not_configured_or_unavailable",
    }

app.include_router(production_router, prefix=settings.api_prefix)
app.include_router(drift_router, prefix=settings.api_prefix)
app.include_router(history_router, prefix=settings.api_prefix)
