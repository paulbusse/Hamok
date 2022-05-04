"""
Keys from the public configuration file
"""
MONITOR = "monitor"
DELAY = "delay"
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
MQTTDEBUG = "mqttdebug"

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
CALLBACK = "callback"
ARGUMENTS = "arguments"
