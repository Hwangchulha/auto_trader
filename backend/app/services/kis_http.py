
import os, httpx
from app.services.kis_auth import get_access_token

BASE = os.getenv("KIS_BASE", "https://openapivts.koreainvestment.com:29443")
APP_KEY = os.environ.get("KIS_APP_KEY","")
APP_SECRET = os.environ.get("KIS_APP_SECRET","")

async def kis_get(path: str, tr_id: str, params: dict):
    token = await get_access_token()
    headers = {
        "authorization": f"Bearer {token}",
        "appkey": APP_KEY,
        "appsecret": APP_SECRET,
        "tr_id": tr_id,
        "custtype": "P",
    }
    async with httpx.AsyncClient(timeout=15) as c:
        r = await c.get(f"{BASE}{path}", headers=headers, params=params)
        r.raise_for_status()
        return r.json()
