import os
from fastapi import APIRouter
router = APIRouter(prefix="/api/settings", tags=["settings"])

@router.get("/runtime")
def runtime():
    # minimal runtime info for frontend settings page
    return {
        "NEXT_PUBLIC_API_BASE": os.environ.get("NEXT_PUBLIC_API_BASE","http://localhost:8000"),
        "SIM_MODE": os.environ.get("SIM_MODE","1"),
        "KIS_ENV": os.environ.get("KIS_ENV","vts"),
        "DEFAULT_TZ": os.environ.get("DEFAULT_TZ","Asia/Seoul"),
    }
