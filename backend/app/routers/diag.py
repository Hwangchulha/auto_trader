import os, json, logging, subprocess, sys, zipfile, datetime
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import FileResponse, PlainTextResponse
from ..services.kis_auth import get_access_token
from ..services.keys_store import exists as keys_exists
router = APIRouter(prefix="/api/diag", tags=["diagnostics"])
def _mask_env(d: dict) -> dict:
    hide = {"KIS_APP_KEY","KIS_APP_SECRET","authorization","appkey","appsecret","hashkey","PASSWORD","TOKEN","SECRET","KEY"}
    out = {}
    for k,v in d.items():
        if any(h.lower() in k.lower() for h in hide): out[k] = "***"
        else: out[k] = v
    return out
LOG_DIR = os.path.abspath(os.environ.get("LOG_DIR","./logs"))
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILES = {n: os.path.join(LOG_DIR, f"{n}.log") for n in ["app","error","access","kis","client"]}
@router.get("/env")
def env():
    return {"resolved_log_dir": LOG_DIR, "files": LOG_FILES, "env": _mask_env(dict(os.environ)), "keys_present": keys_exists()}
@router.get("/ping")
def ping():
    logging.getLogger("app").info("diag.ping"); return {"pong": True}
@router.get("/health")
async def health():
    errs = []; ok_token = False
    try:
        tok = await get_access_token(); ok_token = bool(tok)
    except Exception as e:
        errs.append(f"token:{e}")
    return {"ok": ok_token and len(errs)==0, "kis_token": ok_token, "errors": errs}
@router.get("/logs")
def logs(file: str = Query("app"), tail: int = Query(200)):
    p = LOG_FILES.get(file)
    if not p or not os.path.exists(p):
        raise HTTPException(status_code=404, detail=f"log file not found: {file}")
    with open(p, "r", encoding="utf-8", errors="ignore") as f:
        lines = f.readlines()
    return PlainTextResponse("".join(lines[-tail:]))
@router.get("/bundle")
def bundle():
    ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    name = f"bug_report_{ts}.zip"; path = os.path.join(LOG_DIR, name)
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for key, p in LOG_FILES.items():
            if os.path.exists(p):
                with open(p, "r", encoding="utf-8", errors="ignore") as f: lines = f.readlines()
                z.writestr(f"logs/{key}.log","".join(lines[-5000:]))
        z.writestr("env_summary.json", json.dumps(_mask_env(dict(os.environ)), ensure_ascii=False, indent=2))
        z.writestr("runtime.json", json.dumps({"python": sys.version, "platform": sys.platform}, indent=2))
    return FileResponse(path, filename=name, media_type="application/zip")
