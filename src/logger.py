import config
import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

LOG_OPTIONS = {"ERROR": 0, "WARNING": 1, "INFO": 2}

LOG_OPTION = config.ALFRED_BOT_LOG

def info(info, log_anyway=False):
    if log_anyway or (is_set_log_option() and verify_log_option(LOG_OPTION, "INFO")):
        logger.info(info)
    
def warning(warning, log_anyway=False):
    if log_anyway or (is_set_log_option() and verify_log_option(LOG_OPTION, "WARNING")):
        logger.warning(warning)
    
def error(error, update, context, log_anyway=False):
    if log_anyway or (is_set_log_option() and verify_log_option(LOG_OPTION, "ERROR")):
        logger.error(error, update, context.error)

def verify_log_option(LOG_OPTION, LOG_MODE): 
    return LOG_OPTIONS[LOG_OPTION] >= LOG_OPTIONS[LOG_MODE]

def is_set_log_option():
    return LOG_OPTION in LOG_OPTIONS
    