import logging
import logging.config

from const import LOGGING

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("default")

def changeLogger(l):
    global logger
    
    if not l in LOGGING["loggers"].keys():
        logger.error("{} is not a known logger setting. Using 'default'.".format(l))
        l = "default"
    
    logger = logging.getLogger(l)
    logger.debug("Now using {} logger.".format(l))

def debug(s):
    logger.debug(s)

def info(s):
    logger.info(s)

def error(s):
    logger.error(s)
