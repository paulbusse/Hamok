import atexit
import json
import time
import paho.mqtt.client as mqtt
import sys

import llog
import config

from const import (
    CLIENTID,
    MQTT,
    MQTTHOST,
    MQTTPORT,
)

def stoploop():
    hamqttc.stoploop();

class Mqttc:

    def __init__(self):
        """
        _connected:
            0 -> Not connected
            1 -> succesfully connected
            2 -> connection failed
        """
        self._connected = 0
        self._client = None
        self._clientid = None
        self._cmdtopics = dict()
        self._host = None
        self._port = None

    def configure(self):
        cfg = config.get(MQTT)
        self._clientid = config.get(CLIENTID)
        self._host = cfg[MQTTHOST]
        self._port = cfg[MQTTPORT]

        self._client = mqtt.Client(self._clientid)
        self._client._keepalive = 60 #FIXME: make this configurable
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        self._client.on_message = self.on_message
        self._client._clean_session = False

    def on_connect(self, client, userdata, flags, rc):
        if rc != 0:
            self._connected = 2
            llog.error("Connecting to broker returned {}.".format(rc))
        else:
            self._connected = 1

    def on_disconnect(self, client, userdata, rc):
        self._connected = 0

    def on_message(self, client, userdata, message):
        payload = message.payload.decode('utf-8')
        topic = message.topic
        llog.info("Received {} from {}".format(payload, topic))
        entity = self._cmdtopics[topic]
        entity.set_haval(payload)


    def connect(self):
        try:
            ret = self._client.connect(self._host,self._port)
        except Exception as e:
            llog.error("Failed to connect to MQTT broker at {}:{} : {}".format(self._host, self._port, e))
            sys.exit("MQTT Broker connection")

        atexit.register(stoploop)
        self._client.loop_start()

        while not self._connected:
            time.sleep(0.1)

        llog.info("Connected to MQTT broker at {}:{} as {}.".format(self._host, self._port, self._clientid))


    def stoploop(self):
        llog.debug("Terminating MQTT loop")
        self._client.loop_stop()

    def disconnect(self):
        if not self._connected:
            return
        try:
            self._client.disconnect()
        except Exception as e:
            llog.error(f"Disconnecting from broker failed: {e}")
            return

        while not self._connected:
            time.sleep(0.1)

        llog.info("Disconnected from MQTT broker.")


    def create_entity(self, entity):
        data = json.dumps(entity.control_data())
        topic = entity.createtopic
        try:
            if not self._connected:
                self.connect()
            ret = self._client.publish(topic, payload=data, qos=1, retain=True)
        except Exception as e:
            llog.error("Failed to publish to MQTT topic {}: ".format(topic, e))
            exit()
        llog.info("Defining a new entity for {}[Mid:{}].".format(entity.name, ret.mid))

        ct = entity.cmdtopic
        if ct:
            self._cmdtopics[ct] = entity


    def publish_value(self, topic, v):
        try:
            ret = self._client.publish(topic, payload=v, qos=1, retain=True)
        except Exception as e:
            llog.error(f"Failed to publish to MQTT topic {topic}: {e}")
            return False
        llog.info(f"Sending {v} on {topic}[Mid:{ret.mid}].")
        return True

    def subscribe(self):
        topics = self._cmdtopics
        pmtopics = list(map( lambda x: (x,0), topics))
        try:
            if not self._connected:
                self.connect()

            ret = self._client.subscribe(pmtopics)
        except Exception as e:
            llog.error("Failed to subscribe to topics {}: ".format(topics, e))
            exit()
        llog.info("Subscribing to topics: {}[Mid:{}].".format(list(topics.keys()), ret[1]))


hamqttc = Mqttc()