import os
def get_env(k, d=""): return os.environ.get(k, d)
def kis_base():
    env = get_env("KIS_ENV","vts").lower()
    return "https://openapivts.koreainvestment.com:29443" if env=="vts" else "https://openapi.koreainvestment.com:9443"
def kis_appkey(): return get_env("KIS_APP_KEY","")
def kis_secret(): return get_env("KIS_APP_SECRET","")
def kis_cano(): return get_env("KIS_CANO","")
def kis_acnt(): return get_env("KIS_ACNT_PRDT_CD","01")
