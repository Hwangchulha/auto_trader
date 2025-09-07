
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Symbol

router = APIRouter(prefix="/api", tags=["watchlist"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def infer_market(code: str) -> tuple[str, str]:
    code = code.strip().upper()
    if ":" in code:
        market, raw = code.split(":", 1)
        return market, f"{market}:{raw}"
    if code.isdigit():
        return "KRX", f"KRX:{code}"
    else:
        return "US", f"US:{code}"

@router.get("/watchlist")
def list_watchlist(db: Session = Depends(get_db)):
    rows = db.query(Symbol).order_by(Symbol.code.asc()).all()
    return [{"code": r.code, "market": r.market, "name": r.name, "active": r.active} for r in rows]

@router.post("/watchlist")
def add_symbol(payload: dict, db: Session = Depends(get_db)):
    in_code = payload.get("code", "").strip()
    if not in_code:
        raise HTTPException(status_code=400, detail="code required")
    market, normalized = infer_market(in_code)
    name = payload.get("name", normalized)
    existing = db.query(Symbol).filter(Symbol.code == normalized).first()
    if existing:
        raise HTTPException(status_code=409, detail="symbol exists")
    sym = Symbol(code=normalized, market=market, name=name, active=True)
    db.add(sym); db.commit()
    return {"ok": True, "code": normalized}

@router.patch("/watchlist/{code}")
def update_symbol(code: str, payload: dict, db: Session = Depends(get_db)):
    row = db.query(Symbol).filter(Symbol.code == code).first()
    if not row:
        raise HTTPException(status_code=404, detail="symbol not found")
    if "active" in payload:
        row.active = bool(payload["active"])
    if "name" in payload:
        row.name = str(payload["name"])
    db.add(row); db.commit()
    return {"ok": True}

@router.delete("/watchlist/{code}")
def delete_symbol(code: str, db: Session = Depends(get_db)):
    row = db.query(Symbol).filter(Symbol.code == code).first()
    if not row:
        raise HTTPException(status_code=404, detail="symbol not found")
    db.delete(row); db.commit()
    return {"ok": True}
