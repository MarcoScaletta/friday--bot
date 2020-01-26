import config
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LOG_OPTIONS = {"ERROR": 0, "WARNING": 1, "INFO": 2}

LOG_OPTION = config.ALFRED_BOT_LOG


def info(info_to_log, log_anyway=False):
    if log_anyway or (is_set_log_option() and verify_log_option(LOG_OPTION, "INFO")):
        logger.info(info_to_log)


def warning(warning_to_log, log_anyway=False):
    if log_anyway or (is_set_log_option() and verify_log_option(LOG_OPTION, "WARNING")):
        logger.warning(warning_to_log)


def error(error_to_log, update, context, log_anyway=False):
    if log_anyway or (is_set_log_option() and verify_log_option(LOG_OPTION, "ERROR")):
        logger.error(error_to_log, update, context.error)


def verify_log_option(log_option, log_mode):
    return LOG_OPTIONS[log_option] >= LOG_OPTIONS[log_mode]

def is_set_log_option():
    return LOG_OPTION in LOG_OPTIONS
