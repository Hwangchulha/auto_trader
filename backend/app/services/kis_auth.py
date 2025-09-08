import time, httpx, logging
from .kis_env import kis_base, kis_appkey, kis_secret
log = logging.getLogger("kis")
_token = {"v":"", "exp":0}
def reset_token():
    _token["v"] = ""; _token["exp"] = 0
async def get_access_token() -> str:
    now = int(time.time())
    if _token["v"] and _token["exp"] - 60 > now:
        return _token["v"]
    url = f"{kis_base()}/oauth2/tokenP"
    body = {"grant_type":"client_credentials","appkey":kis_appkey(),"appsecret":kis_secret()}
    async with httpx.AsyncClient(timeout=10.0) as c:
        r = await c.post(url, headers={"content-type":"application/json"}, json=body)
        r.raise_for_status()
        j = r.json()
        _token["v"] = j.get("access_token",""); _token["exp"] = now + 23*3600
        log.info("tokenP ok"); return _token["v"]
async def get_hashkey(body: dict) -> str:
    tok = await get_access_token()
    async with httpx.AsyncClient(timeout=10.0) as c:
        r = await c.post(f"{kis_base()}/uapi/hashkey", headers={
            "content-type":"application/json",
            "authorization": f"Bearer {tok}",
            "appkey": kis_appkey(),
            "appsecret": kis_secret(),
        }, json=body)
        r.raise_for_status(); d = r.json(); return d.get("HASH") or d.get("hashkey","")
