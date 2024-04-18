import logging
import os
from smct import paths

LOGFILENAME = paths.LOG_PATH
ENCODING = "utf-8"

LOG = None
STARTUP = True

LOG_LINE_LIMIT = 300


def log(text):
    LOG.info(text)


def clear_log_if_needed():
    if os.path.exists(LOGFILENAME):
        with open(LOGFILENAME, "r", encoding=ENCODING) as file:
            lines = file.readlines()
            if len(lines) > LOG_LINE_LIMIT:
                with open(LOGFILENAME, "w", encoding=ENCODING) as file:
                    file.write("")


if STARTUP:
    clear_log_if_needed()
    logging.basicConfig(
        filename=LOGFILENAME,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    LOG = logging.getLogger(__name__)
    LOG.critical("Start")
    STARTUP = False
