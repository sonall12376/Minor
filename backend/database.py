from collections.abc import Generator
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session, sessionmaker
from backend.config import settings

engine = create_engine(
    settings.database_url, pool_pre_ping=True, pool_recycle=1800, echo=False
) if settings.database_url else None

SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False) if engine else None

def get_db() -> Generator[Session, None, None]:
    if SessionLocal is None:
        raise RuntimeError("DATABASE_URL is not configured. Add it to .env.")
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_database() -> bool:
    if engine is None:
        return False
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
    return True
