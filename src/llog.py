import logging
import logging.config
import sys

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            '%(asctime)s %(levelname)-10s %(threadName)s: %(message)s'
        },
        'syslog': {
            'format': 'hamok[%(process)d] %(levelname)-8s %(threadName)s: %(message)s'
        },
        'simple': {
            'format': '%(message)s'
        }
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'formatter': 'verbose',
        },
        'interactive': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
            'formatter': 'simple',
        },
        'sys-logger0': {
            'class': 'logging.handlers.SysLogHandler',
            'address': "/dev/log",
            'facility': "local0",
            'formatter': 'syslog',
            'level': logging.INFO
        },
    },
    'loggers': {
        'devel': {
            'handlers': ['sys-logger0', 'stderr'],
            'level': logging.DEBUG,
            'propagate': True,
        },
        'default': {
            'handlers': ['sys-logger0'],
            'level': logging.INFO,
            'propagate': True,
        },
        'debug': {
            'handlers': ['sys-logger0'],
            'level': logging.DEBUG,
            'propagate': True,
        },
        'interactive': {
            'handlers': ['interactive'],
            'level': logging.INFO,
            'propagate': True,
        },
    }
}

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("interactive")

def changeLogger(l):
    global logger

    if not l in LOGGING["loggers"].keys():
        logger.error(f"{l} is not a known logger setting. Using 'default'.")
        l = "default"

    logger = logging.getLogger(l)
    logger.debug(f"Now using {l} logger.")

def debug(s):
    logger.debug(s)

def info(s):
    logger.info(s)

def error(s):
    logger.error(s)

def fatal(s):
    logger.fatal(s + " Exiting.")
    sys.exit(1)
