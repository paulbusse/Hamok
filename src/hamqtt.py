import os
import json
import datetime
import paho.mqtt.client as mqtt

import llog
import config
from const import (
    CLIENTID,
    COMPONENT,
    MQTT,
    MQTTHOST,
    MQTTPORT,
)

mqttc = None

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
    clientid = config.get(CLIENTID)
    mqtthost = cfg[MQTTHOST]
    mqttport = cfg[MQTTPORT]
   
    mqttc = mqtt.Client(clientid)
    mqttc._keepalive = 60 #TODO: make this configurable
    mqttc.on_connect = on_connect
    mqttc.on_disconnect = on_disconnect
    mqttc._clean_session = False
    
    try:
        mqttc.connect(mqtthost,mqttport)
    except Exception as e:
        llog.error("Failed to connect to MQTT broker at {}:{} : {}".format(mqtthost, mqttport, e))
        exit()
    
    llog.info("Connected to MQTT broker at {}:{} as {}.".format(mqtthost, mqttport, clientid))
    

def create_entity(entity):
    data = json.dumps(entity.control_data())
    topic = entity.createtopic
    try:
        if not flag_connected:
            connect()

        mqttc.publish(topic, payload=data, qos=1, retain=True)
    except Exception as e:
        llog.error("Failed to publish to MQTT topic {}: ".format(topic, e))
        exit()    
    llog.info("Defining a new entity for {}.".format(entity.name))
    
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

        mqttc.publish(topic, payload=jdata, qos=1, retain=True)
        llog.debug("Sending {} on {}.".format(jdata, topic))
    except Exception as e:
        llog.error("Failed to publish to MQTT topic {}: ".format(topic, e))
        exit()    
    llog.info("Setting the value of entity {} to {}.".format(entity.name, v))
    