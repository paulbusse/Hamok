import os
import json
import datetime
import logging
import paho.mqtt.client as mqtt

import config
from const import (
    COMPONENT,
    MQTT,
    MQTTHOST,
    MQTTPORT,
)

mqttc = None

logger = logging.getLogger("default")

flag_connected = 0

def on_connect(client, userdata, flags, rc):
   global flag_connected
   flag_connected = 1

def on_disconnect(client, userdata, rc):
   global flag_connected
   flag_connected = 0

def connect():
    global mqttc
    component = config.get(COMPONENT)
    cfg = config.get(MQTT)
    mqtthost = cfg[MQTTHOST]
    mqttport = cfg[MQTTPORT]
   
    clientid = component + str(os.getpid())
    
    mqttc = mqtt.Client(clientid)
    mqttc._keepalive = 60 #TODO: make this configurable
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    try:
        mqttc.connect(mqtthost,mqttport)
    except Exception as e:
        logger.error("Failed to connect to MQTT broker at {}:{} : {}".format(mqtthost, mqttport, e))
        exit()
    
    logger.info("Connected to MQTT broker at {}:{} as {}.".format(mqtthost, mqttport, clientid))
    

def create_entity(entity):
    data = json.dumps(entity.control_data())
    topic = entity.createtopic
    try:
        if not flag_connected:
            connect()

        mqttc.publish(topic, payload=data, qos=0, retain=True)
    except Exception as e:
        logger.error("Failed to publish to MQTT topic {}: ".format(topic, e))
        exit()    
    logger.info("Defining a new entity for {}.".format(entity.name))
    
def publish_value(entity):
    data = {}
    v = entity.get_haval()
    data['val'] = v
    data['last_update'] = datetime.datetime.now().replace(microsecond=0).isoformat()
    jdata = json.dumps(data)
    topic = entity.statetopic
    try:
        if not flag_connected:
            connect()

        mqttc.publish(topic, payload=jdata, qos=0, retain=True)
        logger.debug("Sending {} on {}.".format(jdata, topic))
    except Exception as e:
        logger.error("Failed to publish to MQTT topic {}: ".format(topic, e))
        exit()    
    logger.info("Setting the value of entity {} to {}.".format(entity.name, v))
    