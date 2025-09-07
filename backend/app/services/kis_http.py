import httpx, logging
from typing import Dict, Any
from .kis_env import kis_base, kis_appkey, kis_secret
from .kis_auth import get_access_token, get_hashkey

log = logging.getLogger("kis")
TR_VTS = {
    "order_cash_buy": "VTTC0802U",
    "order_cash_sell": "VTTC0801U",
    "balance": "VTTC8434R",
    "psbl_order": "VTTC8908R",
    "price": "FHKST01010100",
}
TR_PROD = {
    "order_cash_buy": "TTTC0802U",
    "order_cash_sell": "TTTC0801U",
    "balance": "TTTC8434R",
    "psbl_order": "TTTC8908R",
    "price": "FHKST01010100",
}

def kis_env()->str:
    import os
    return os.environ.get("KIS_ENV","vts").lower()

def tr_id(key:str)->str:
    return (TR_VTS if kis_env()=="vts" else TR_PROD).get(key,"")

async def kis_get(path: str, tr_key: str, params: Dict[str, Any]) -> Dict[str,Any]:
    tok = await get_access_token()
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {tok}",
        "appkey": kis_appkey(),
        "appsecret": kis_secret(),
        "tr_id": tr_id(tr_key),
        "custtype": "P"
    }
    url = f"{kis_base()}{path}"
    async with httpx.AsyncClient(timeout=15.0) as c:
        log.debug("GET %s tr=%s params=%s", path, tr_key, params)
        r = await c.get(url, headers=headers, params=params)
        r.raise_for_status()
        j = r.json()
        log.debug("GET ok %s rt_cd=%s msg_cd=%s", path, j.get("rt_cd"), j.get("msg_cd"))
        return j

async def kis_post(path: str, tr_key: str, body: Dict[str,Any])->Dict[str,Any]:
    tok = await get_access_token()
    hkey = await get_hashkey(body)
    headers = {
        "content-type": "application/json",
        "authorization": f"Bearer {tok}",
        "appkey": kis_appkey(),
        "appsecret": kis_secret(),
        "tr_id": tr_id(tr_key),
        "custtype": "P",
        "hashkey": hkey
    }
    url = f"{kis_base()}{path}"
    async with httpx.AsyncClient(timeout=15.0) as c:
        log.info("POST %s tr=%s body_keys=%s", path, tr_key, list(body.keys()))
        r = await c.post(url, headers=headers, json=body)
        r.raise_for_status()
        j = r.json()
        log.info("POST ok %s rt_cd=%s msg_cd=%s", path, j.get("rt_cd"), j.get("msg_cd"))
        return j
