
import os, json, httpx, asyncio
from app.services.kis_auth import get_access_token, hashkey

BASE = os.getenv("KIS_BASE", "https://openapivts.koreainvestment.com:29443")
APP_KEY = os.environ.get("KIS_APP_KEY")
APP_SECRET = os.environ.get("KIS_APP_SECRET")
CANO = os.environ.get("KIS_CANO", "")
ACNT_PRDT_CD = os.environ.get("KIS_ACNT_PRDT_CD","01")

async def order_cash(symbol:str, side:str, qty:int, price:float|None=None):
    token = await get_access_token()
    tr_id = "VTTC0802U" if side=="buy" else "VTTC0801U"  # 모의; 실전은 TTTC*
    ord_dvsn = "01" if price is None else "00"
    body = {"CANO": CANO,"ACNT_PRDT_CD": ACNT_PRDT_CD,"PDNO": symbol,"ORD_DVSN": ord_dvsn,"ORD_QTY": str(int(qty)),"ORD_UNPR": "0" if price is None else str(price)}
    hkey = await hashkey(body)
    headers = {"content-type":"application/json","authorization": f"Bearer {token}","appkey": APP_KEY or "","appsecret": APP_SECRET or "","tr_id": tr_id,"custtype":"P","hashkey": hkey}
    async with httpx.AsyncClient(timeout=10) as c:
        r = await c.post(f"{BASE}/uapi/domestic-stock/v1/trading/order-cash", headers=headers, data=json.dumps(body))
        r.raise_for_status(); return r.json()
