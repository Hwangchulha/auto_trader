import os, logging, sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
def _resolve_dir():
    cand = [os.environ.get("LOG_DIR"), "./logs", "/tmp/logs"]
    for c in cand:
        if not c: continue
        try:
            Path(c).mkdir(parents=True, exist_ok=True)
            Path(c, ".touch").write_text("ok", encoding="utf-8")
            return os.path.abspath(c)
        except Exception:
            continue
    return os.path.abspath("./logs")
def _handler(path, level):
    h = RotatingFileHandler(path, maxBytes=int(os.environ.get("LOG_MAX_BYTES","5242880")),
                            backupCount=int(os.environ.get("LOG_BACKUP_COUNT","5")), encoding="utf-8")
    fmt = logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s')
    h.setFormatter(fmt); h.setLevel(level)
    return h
def setup_logging():
    level = getattr(logging, os.environ.get("LOG_LEVEL","INFO").upper(), logging.INFO)
    to_stdout = str(os.environ.get("LOG_TO_STDOUT","1")).lower() in ("1","true","yes")
    log_dir = _resolve_dir()
    root = logging.getLogger()
    root.setLevel(level)
    if to_stdout:
        sh = logging.StreamHandler(sys.stdout)
        sh.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(name)s %(message)s'))
        sh.setLevel(level)
        root.addHandler(sh)
    app_file    = _handler(os.path.join(log_dir, "app.log"), level)
    error_file  = _handler(os.path.join(log_dir, "error.log"), logging.ERROR)
    access_file = _handler(os.path.join(log_dir, "access.log"), level)
    kis_file    = _handler(os.path.join(log_dir, "kis.log"), level)
    client_file = _handler(os.path.join(log_dir, "client.log"), level)
    logging.getLogger("app").addHandler(app_file)
    logging.getLogger("app").addHandler(error_file)
    logging.getLogger("uvicorn.access").addHandler(access_file)
    logging.getLogger("uvicorn.error").addHandler(app_file)
    logging.getLogger("kis").addHandler(kis_file)
    logging.getLogger("client").addHandler(client_file)
    logging.getLogger("app").info("Logging initialized. dir=%s level=%s", log_dir, logging.getLevelName(level))
