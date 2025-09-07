
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.schemas import RuntimeSettingsIn
from app.services.runtime_settings import get_runtime, set_many

router = APIRouter(prefix="/api/settings", tags=["settings"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/runtime")
def runtime(db: Session = Depends(get_db)):
    return get_runtime(db)

@router.put("/runtime")
def update_runtime(payload: RuntimeSettingsIn, db: Session = Depends(get_db)):
    updates = {k: v for k,v in payload.model_dump().items() if v is not None}
    after = set_many(db, updates)
    return {"ok": True, "settings": after}
