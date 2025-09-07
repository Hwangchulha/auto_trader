
from app.config import settings
from app.services.kis_http import kis_get

async def fetch_domestic_balance():
    if not settings.KIS_TR_DOM_BAL_PATH or not settings.KIS_TR_DOM_BAL_ID:
        return None
    params = {"CANO": settings.KIS_CANO, "ACNT_PRDT_CD": settings.KIS_ACNT_PRDT_CD}
    try:
        return await kis_get(settings.KIS_TR_DOM_BAL_PATH, settings.KIS_TR_DOM_BAL_ID, params)
    except Exception as e:
        return {"error": str(e)}

async def fetch_domestic_deposit():
    if not settings.KIS_TR_DOM_DEPOSIT_PATH or not settings.KIS_TR_DOM_DEPOSIT_ID:
        return None
    params = {"CANO": settings.KIS_CANO, "ACNT_PRDT_CD": settings.KIS_ACNT_PRDT_CD}
    try:
        return await kis_get(settings.KIS_TR_DOM_DEPOSIT_PATH, settings.KIS_TR_DOM_DEPOSIT_ID, params)
    except Exception as e:
        return {"error": str(e)}

async def fetch_overseas_balance():
    if not settings.KIS_TR_OS_BAL_PATH or not settings.KIS_TR_OS_BAL_ID:
        return None
    params = {"CANO": settings.KIS_CANO, "ACNT_PRDT_CD": settings.KIS_ACNT_PRDT_CD}
    try:
        return await kis_get(settings.KIS_TR_OS_BAL_PATH, settings.KIS_TR_OS_BAL_ID, params)
    except Exception as e:
        return {"error": str(e)}
