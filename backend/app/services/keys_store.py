import time
from typing import Optional, Dict
from sqlalchemy.orm import Session
from ..db import SessionLocal
from ..models import KISKey
_cache = {"v": None, "t": 0}
def _now() -> float: return time.time()
def load_keys() -> Optional[Dict]:
    if _cache["v"] and _now() - _cache["t"] < 10:
        return _cache["v"]
    db = SessionLocal()
    try:
        row = db.query(KISKey).order_by(KISKey.id.desc()).first()
        if not row:
            _cache["v"] = None
        else:
            _cache["v"] = {
                "app_key": row.app_key or "",
                "app_secret": row.app_secret or "",
                "cano": row.cano or "",
                "acnt_prdt_cd": row.acnt_prdt_cd or "01",
                "kis_env": (row.kis_env or "vts").lower(),
            }
        _cache["t"] = _now()
        return _cache["v"]
    finally:
        db.close()
def save_keys(data: Dict) -> Dict:
    db = SessionLocal()
    try:
        row = db.query(KISKey).order_by(KISKey.id.desc()).first()
        if not row:
            row = KISKey(); db.add(row)
        row.app_key = data.get("app_key","")
        row.app_secret = data.get("app_secret","")
        row.cano = data.get("cano","")
        row.acnt_prdt_cd = data.get("acnt_prdt_cd","01")
        row.kis_env = (data.get("kis_env","vts") or "vts").lower()
        db.commit(); _cache["v"] = None
        return {"ok": True}
    finally:
        db.close()
def exists() -> bool:
    return load_keys() is not None
def mask(s: str) -> str:
    if not s: return s
    if len(s) <= 6: return "***"
    return s[:3] + "***" + s[-3:]
