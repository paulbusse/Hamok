import sys
import logging
import enum

"""
Keys from the public configuration file
"""
MONITOR = "monitor"
MQTT = "mqtt"
OEKOFEN = "oekofen"
HOST = "host"
JSONPORT = "jsonport"
JSONPWD = "jsonpassword"
MQTTHOST = "broker"
MQTTPORT = "port"
INTERVAL = "interval"
DEVICE = "device"
CLIENTID = "clientid"
LOGGER= "logger"

""" Entity Types """
BINARYSENSOR = "binary_sensor"
NUMBER = "number"
SELECT = "select"
SENSOR = "sensor"
SWITCH = "switch"

""" Ökofen JSON keys """
VAL = "val"
UNIT = "unit"
FACTOR = "factor"
MINIMUM = "min"
MAXIMUM = "max"
FORMAT = "format"

""" Ökofen JSON labels """
NAME = "name"

""" formats that mean on/off """
ONOFFFORMATS = [
    "0:Uit|1:Aan",    # Dutch
    "0:Off|1:On",     # English
]


""" HA Basic configuration """
TOPICROOT = 'homeassistant/'


""" Internal Config keys """
COMPONENT = "__device"

""" Default Configuration """
DEFAULTCONFIG = {
    CLIENTID: "hamok",
    LOGGER: "default",
    MQTT: {
        MQTTPORT: 1883
    },
    OEKOFEN: {
        HOST: None,
        JSONPORT: None,
        JSONPWD: None,
    },
    MONITOR: [],
    INTERVAL: 60,
    DEVICE: "Oekofen"
}


""" JOB IDS"""
JOBID = "jobid"
ENTITY = "entity"
PAYLOAD = "payload"
CALLBACK = "callback"
ARGUMENTS = "arguments"
class JobID(enum.Enum):
    ALL = 1
    UPDATE = 2
    SCHEDULE = 3


""" LOGGING CONFIG """
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format':
            '%(asctime)s %(levelname)-10s %(message)s'
        },
        'syslog': {
            'format': 'hamok[%(process)d] %(levelname)-8s %(message)s'
        }
    },
    'handlers': {
        'stderr': {
            'class': 'logging.StreamHandler',
            'stream': sys.stderr,
            'formatter': 'verbose',
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
    }
}