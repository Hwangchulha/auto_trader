import os
from fastapi import APIRouter
from ..services.keys_store import exists as keys_exists

router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/runtime")
def runtime():
    return {
        "NEXT_PUBLIC_API_BASE": os.environ.get("NEXT_PUBLIC_API_BASE","http://localhost:8000"),
        "SIM_MODE": os.environ.get("SIM_MODE","1"),
        "KIS_ENV": os.environ.get("KIS_ENV","vts"),
        "DEFAULT_TZ": os.environ.get("DEFAULT_TZ","Asia/Seoul"),
        "needs_keys": not keys_exists()
    }
