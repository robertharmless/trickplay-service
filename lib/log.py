"""
Logging Processes
"""
# Built-in
import logging

# App
from .config import App
from .config import Logs

app = App()
logs = Logs()

# create logger
logger = logging.getLogger(f"{logs.log_file_path}")
logger.setLevel(logs.loglevel)

fh = logging.FileHandler(f"{logs.log_file_path}")
fh.setLevel(logs.loglevel)

ch = logging.StreamHandler()
ch.setLevel(logs.loglevel)

formatter = logging.Formatter("%(asctime)s %(levelname)9s %(process)d : %(message)s")
fh.setFormatter(formatter)
ch.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)


def log_debug(msg: str):
    logger.debug(f"{msg}")


def log_info(msg: str):
    logger.info(f"{msg}")


def log_error(msg: str):
    logger.error(f"{msg}")


def log_exception(msg: str):
    logger.exception(f"{msg}")
