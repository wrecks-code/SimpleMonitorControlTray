import logging
import os
from smct.paths import LOG_PATH

ENCODING = "utf-8"
INFO = "info"
ERROR = "error"

LOG = None
STARTUP = True

LOG_LINE_LIMIT = 300


def log(log_type, text):
    if log_type == ERROR:
        LOG.error(text)
    elif log_type == INFO:
        LOG.info(text)


def clear_log_if_needed():
    if os.path.exists(LOG_PATH):
        with open(LOG_PATH, "r", encoding=ENCODING) as file:
            lines = file.readlines()
            if len(lines) > LOG_LINE_LIMIT:
                with open(LOG_PATH, "w", encoding=ENCODING) as file:
                    file.write("")


if STARTUP:
    clear_log_if_needed()
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    LOG = logging.getLogger(__name__)
    LOG.critical("Program startup")
    STARTUP = False
