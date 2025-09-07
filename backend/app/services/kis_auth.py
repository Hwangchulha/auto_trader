
import os, json, time, httpx

BASE = os.getenv("KIS_BASE", "https://openapivts.koreainvestment.com:29443")
APP_KEY = os.environ.get("KIS_APP_KEY")
APP_SECRET = os.environ.get("KIS_APP_SECRET")

_token_cache = {"token": None, "exp": 0}

async def get_access_token():
    now = time.time()
    if _token_cache["token"] and _token_cache["exp"] - now > 300:
        return _token_cache["token"]
    body = {"grant_type": "client_credentials", "appkey": APP_KEY, "appsecret": APP_SECRET}
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.post(f"{BASE}/oauth2/tokenP", headers={"content-type":"application/json"}, data=json.dumps(body))
        r.raise_for_status(); j = r.json()
    _token_cache["token"] = j["access_token"]
    _token_cache["exp"] = now + 23*3600
    return _token_cache["token"]
