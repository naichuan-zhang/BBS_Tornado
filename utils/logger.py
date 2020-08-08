import logging
import logging.config

from config import LOGGING


def logger(name):
    logging.config.dictConfig(LOGGING)
    try:
        log = logging.getLogger(name)
    except Exception as e:
        raise e
    return log
