import os
from .keys_store import load_keys

def get_env(k, d=""): return os.environ.get(k, d)

def kis_env():
    k = load_keys()
    if k and k.get("kis_env"): return k["kis_env"]
    return get_env("KIS_ENV","vts").lower()

def kis_base():
    env = kis_env()
    return "https://openapivts.koreainvestment.com:29443" if env=="vts" else "https://openapi.koreainvestment.com:9443"

def kis_appkey():
    k = load_keys()
    if k and k.get("app_key"): return k["app_key"]
    return get_env("KIS_APP_KEY","")

def kis_secret():
    k = load_keys()
    if k and k.get("app_secret"): return k["app_secret"]
    return get_env("KIS_APP_SECRET","")

def kis_cano():
    k = load_keys()
    if k and k.get("cano"): return k["cano"]
    return get_env("KIS_CANO","")

def kis_acnt():
    k = load_keys()
    if k and k.get("acnt_prdt_cd"): return k["acnt_prdt_cd"]
    return get_env("KIS_ACNT_PRDT_CD","01")

def sim_mode():
    return str(get_env("SIM_MODE","1")).lower() in ("1","true","yes")
