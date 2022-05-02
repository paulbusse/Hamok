import atexit
import json
import time
import paho.mqtt.client as mqtt

import llog
import config

from servicestate import servicestate

from const import (
    CLIENTID,
    MQTT,
    MQTTDEBUG,
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
        self._gotcallback = False
        self._connected = False
        self._client = None
        self._clientid = None
        self._subscriptions = dict()
        self._host = None
        self._port = None

    def configure(self, callback):
        cfg = config.get(MQTT)
        self._clientid = config.get(CLIENTID)
        self._host = cfg[MQTTHOST]
        self._port = cfg[MQTTPORT]
        self._connectcallback = callback
        self._debug = config.get(MQTTDEBUG)

        self._client = mqtt.Client(self._clientid)
        self._client._keepalive = 60 #FIXME: make this configurable
        self._client._clean_session = False
        self._client.on_connect = self.on_connect
        self._client.on_disconnect = self.on_disconnect
        self._client.on_message = self.on_message
        self._client.on_publish = self.on_publish
        self._client.on_subscribe = self.on_subscribe
        self._client.on_log = self.on_log


    def on_log(self, client, userdata, level, buf):
        if self._debug:
            llog.debug(buf)

    def on_connect(self, client, userdata, flags, rc):
        self._connected = True
        self._gotcallback = True
        if rc != 0:
            llog.error(f"Connecting to broker returned {rc}.")
            self._connected = False

        servicestate.mqtt(self._connected)

        if self._connected:
            if self._connectcallback():
                self._connectcallback()


    def on_disconnect(self, client, userdata, rc):
        llog.error("Hamok is disconnected from MQTT Broker")
        servicestate.mqtt(False)


    def on_message(self, client, userdata, message):
        servicestate.mqtt(True)
        payload = message.payload.decode('utf-8')
        topic = message.topic
        llog.info(f"Received {payload} from {topic}.")
        entity = self._subscriptions[topic]
        entity.set_haval(payload)


    def on_publish(self, client, userdata, mid):
        servicestate.mqtt(True)


    def on_subscribe(self, client, userdata, mid, granted_qos):
        servicestate.mqtt(True)


    def connect(self):
        if self._connected:
            return True

        try:
            ret = self._client.connect(self._host,self._port)
        except Exception as e:
            llog.error(f"Failed to connect to MQTT broker at {self._host}:{self._port} : {e}.")
            servicestate.mqtt(False)
            return False

        atexit.register(stoploop)
        self._client.loop_start()

        while not self._gotcallback:
            time.sleep(0.1)

        if(self._connected):
            llog.info(f"Connected to MQTT broker at {self._host}:{self._port} as {self._clientid}.")

        return self._connected


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

        while not self._gotcallback:
            time.sleep(0.1)

        llog.info("Disconnected from MQTT broker.")


    def create_entity(self, entity):
        data = json.dumps(entity.control_data())
        topic = entity.createtopic
        try:
            ret = self._client.publish(topic, payload=data, qos=1, retain=True)
        except Exception as e:
            llog.error(f"Failed to publish to MQTT topic {topic}: {e}.")
            exit()
        llog.info(f"Defining a new entity for {entity.name}[Mid:{ret.mid}].")

        ct = entity.cmdtopic
        if ct:
            self._subscriptions[ct] = entity


    def publish_value(self, topic, v):
        try:
            ret = self._client.publish(topic, payload=v, qos=1, retain=True)
        except Exception as e:
            llog.error(f"Failed to publish to MQTT topic {topic}: {e}")
            return False
        llog.info(f"Sending {v} on {topic}[Mid:{ret.mid}].")
        return True

    def subscribe(self):
        topics = self._subscriptions
        if len(topics) == 0:
            return

        pmtopics = list(map( lambda x: (x,0), topics))
        try:
            ret = self._client.subscribe(pmtopics)
        except Exception as e:
            llog.error(f"Failed to subscribe to topics {topics.keys()}: {e}.")
            exit()
        llog.info(f"Subscribing to topics: {list(topics.keys())}[Mid:{ret[1]}].")


hamqttc = Mqttc()