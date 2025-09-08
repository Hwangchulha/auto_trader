from fastapi import APIRouter, Request
from ..services.keys_store import load_keys, save_keys, exists, mask
from ..services.kis_auth import reset_token

router = APIRouter(prefix="/api/keys", tags=["keys"])

@router.get("/status")
def status():
    k = load_keys()
    return {"exists": bool(k), "env": (k or {}).get("kis_env","")}

@router.get("")
def get_keys_masked():
    k = load_keys()
    if not k:
        return {"exists": False}
    return {
        "exists": True,
        "kis_env": k.get("kis_env","vts"),
        "app_key": mask(k.get("app_key","")),
        "app_secret": mask(k.get("app_secret","")),
        "cano": mask(k.get("cano","")),
        "acnt_prdt_cd": k.get("acnt_prdt_cd","01"),
    }

@router.post("")
async def set_keys(req: Request):
    ctype = (req.headers.get("content-type") or "").lower()
    if "application/json" in ctype:
        data = await req.json()
    else:
        body = (await req.body()).decode()
        from urllib.parse import parse_qs
        d = parse_qs(body)
        data = {k: (v[0] if isinstance(v, list) else v) for k, v in d.items()}
    save_keys({
        "kis_env": data.get("kis_env","vts"),
        "app_key": data.get("app_key",""),
        "app_secret": data.get("app_secret",""),
        "cano": data.get("cano",""),
        "acnt_prdt_cd": data.get("acnt_prdt_cd","01"),
    })
    reset_token()
    return {"ok": True, "saved": True}
