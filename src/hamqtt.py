import os
import json
import datetime
import paho.mqtt.client as mqtt

import llog
import config
from const import (
    CLIENTID,
    MQTT,
    MQTTHOST,
    MQTTPORT,
)

class Mqttc:

    def __init__(self):
        self._connected = False
        self._client = None

    def on_connect(self, client, userdata, flags, rc):
        self._connected = True

    def on_disconnect(self, client, userdata, rc):
        self._connected = False

    def on_message(self, client, userdata, message):
        payload = message.payload.decode('utf-8')
        topic = message.topic
        llog.info("Received {} from {}".format(payload, topic))

    def connect(self):
        cfg = config.get(MQTT)
        clientid = config.get(CLIENTID)
        mqtthost = cfg[MQTTHOST]
        mqttport = cfg[MQTTPORT]

        self._client = mqtt.Client(clientid)
        self._client._keepalive = 60 #TODO: make this configurable
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        self._client.on_message = self.on_message
        self._client._clean_session = False

        try:
            self._client.connect(mqtthost,mqttport)
            self._client.loop_start()
        except Exception as e:
            llog.error("Failed to connect to MQTT broker at {}:{} : {}".format(mqtthost, mqttport, e))
            exit()

        llog.info("Connected to MQTT broker at {}:{} as {}.".format(mqtthost, mqttport, clientid))


    def create_entity(self, entity):
        data = json.dumps(entity.control_data())
        topic = entity.createtopic
        try:
            if not self._connected:
                self.connect()

            self._client.publish(topic, payload=data, qos=1, retain=True)
        except Exception as e:
            llog.error("Failed to publish to MQTT topic {}: ".format(topic, e))
            exit()
        llog.info("Defining a new entity for {}.".format(entity.name))

    def publish_value(self, entity):
        v = entity.get_haval()
        topic = entity.statetopic
        try:
            if not self._connected:
                self.connect()

            self._client.publish(topic, payload=v, qos=1, retain=True)
            llog.debug("Sending {} on {}.".format(v, topic))
        except Exception as e:
            llog.error("Failed to publish to MQTT topic {}: ".format(topic, e))
            exit()
        llog.info("Setting the value of entity {} to {}.".format(entity.name, v))

mqttc = Mqttc()