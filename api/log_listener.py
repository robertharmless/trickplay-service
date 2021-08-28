from lib.log import log_debug, log_info, log_error, log_exception
from api.event import subscribe


def handle_log_debug(who, msg):
    log_debug(f"{who}: {msg}")


def handle_log_info(who, msg):
    log_info(f"{who}: {msg}")


def handle_log_error(who, msg):
    log_error(f"{who}: {msg}")


def handle_log_exception(who, msg):
    log_exception(f"{who}: {msg}")


def setup_log_event_handlers():
    subscribe("log_debug", handle_log_debug)
    subscribe("log_info", handle_log_info)
    subscribe("log_error", handle_log_error)
    subscribe("log_exception", handle_log_exception)
