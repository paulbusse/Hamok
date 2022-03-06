import sys
import logging

""" 
Keys from the configuration file
"""
MONITOR = "monitor"
COMPONENT = "device"
MQTT = "mqtt"
OEKOFEN = "oekofen"
HOST = "host"
JSONPORT = "jsonport"
JSONPWD = "jsonpassword"
MQTTHOST = "broker"
MQTTPORT = "port"
INTERVAL = "interval"
DEVICE = "device"

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


""" Config keys """
LIST = "__list"
DAEMON = "__daemon"
PRINT = "__print"
CLIENTID = "clientid"


""" Default Configuration """
DEFAULTCONFIG = {
    CLIENTID: "hamok",
    DAEMON: True,
    LIST: False,
    PRINT: False,
    MQTT: {
        MQTTPORT: 1883
    },
    INTERVAL: 60,
    DEVICE: "oekofen"
}


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
            'format': 'OkofenMqtt[%(process)d] %(levelname)-10s %(message)s'
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
        'default': {
            'handlers': ['sys-logger0', 'stderr'],
            'level': logging.DEBUG,
            'propagate': True, 
        },
    }
}