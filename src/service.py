import atexit
import time

import entitylist
import config
import llog

from oekofen import oekofenc
from hamqtt import hamqttc
from servicestate import servicestate
from const import COMPONENT, INTERVAL, OFFLINE, ONLINE

def _mqttdisconnect():
    hamqttc.disconnect()

class Service:
    def __init__(self):
        self._connecttopic = None
        self._firstrun = True

    @property
    def connecttopic(self):
        return self._connecttopic

    def configure(self):
        component = config.get(COMPONENT)
        self._connecttopic = f"hamok/{component}/connection"

        hamqttc.configure(self.on_mqttconnect)
        oekofenc.configure()

        while servicestate.ok() and not hamqttc.connect():
            time.sleep(60) #FIXME make this configurable

        if not servicestate.ok():
            llog.fatal(f"Could not connect to MQTT Broker.")

        atexit.register(_mqttdisconnect)

    def on_mqttconnect(self):
        hamqttc.publish_value(self._connecttopic, ONLINE)
        entitylist.create_entities()
        hamqttc.subscribe()


    def run(self):
        interval = config.get(INTERVAL)

        while servicestate.ok():
            oekofenc.load()
            time.sleep(interval)

        if not servicestate.ok():
            llog.error(servicestate.report())

        if not servicestate.oekofen_ok():
            hamqttc.publish_value(self._connecttopic, OFFLINE)


servicec = Service()