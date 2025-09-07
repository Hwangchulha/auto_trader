
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.services.account_engine import get_overview, list_positions, list_orders, list_executions, kis_raw_bundle

router = APIRouter(prefix="/api", tags=["account"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/account/overview")
def overview(db: Session = Depends(get_db)):
    return get_overview(db)

@router.get("/account/positions")
def positions(db: Session = Depends(get_db)):
    return list_positions(db)

@router.get("/account/orders")
def orders(limit: int = Query(50), db: Session = Depends(get_db)):
    return list_orders(db, limit=limit)

@router.get("/account/executions")
def executions(limit: int = Query(50), db: Session = Depends(get_db)):
    return list_executions(db, limit=limit)

@router.get("/account/kis/raw")
def kis_raw(db: Session = Depends(get_db)):
    return kis_raw_bundle(db)
