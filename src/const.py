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


""" HA Values """
OFFLINE = 'offline'
ONLINE = 'online'
OFF = 'off'
ON = 'on'


""" HA Basic configuration """
TOPICROOT = 'homeassistant/'


""" Internal Config keys """
COMPONENT = "__device"


""" JOB IDS"""
JOBID = "jobid"
ENTITY = "entity"
PAYLOAD = "payload"
CALLBACK = "callback"
ARGUMENTS = "arguments"
class JobID(enum.Enum):
    UPDATE = 2
    SCHEDULE = 3
