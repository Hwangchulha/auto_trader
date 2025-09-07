import time, logging, os
from app.logging_setup import setup_logging
setup_logging()
log = logging.getLogger("app")

def main():
    log.info("worker loop started")
    while True:
        log.info("worker heartbeat pid=%s", os.getpid())
        time.sleep(30)

if __name__ == "__main__":
    main()
