
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.ai_engine import get_latest_ai

router = APIRouter(prefix="/api", tags=["ai"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ai/{symbol}")
def ai(symbol: str, db: Session = Depends(get_db)):
    return get_latest_ai(db, symbol)
