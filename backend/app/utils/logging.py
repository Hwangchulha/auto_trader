
import structlog, logging, sys
def get_logger():
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    return structlog.get_logger()
