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
        self._booting = True

    @property
    def connecttopic(self):
        return self._connecttopic


    def _on_connect(self):
        if not self._booting:
            hamqttc.publish_value(self._connecttopic, ONLINE)
            entitylist.create_entities()
            entitylist.report_entities()
            hamqttc.subscribe()


    def configure(self):
        component = config.get(COMPONENT)
        self._connecttopic = f"hamok/{component}/connection"
        hamqttc.configure(self._on_connect)
        oekofenc.configure()


    def run(self):
        interval = config.get(INTERVAL)

        mqttc = hamqttc.connect()
        okfl  = oekofenc.load(False)
        while servicestate.ok() and not mqttc and not okfl:
            time.sleep(interval)
            mqttc = hamqttc.connect()
            okfl  = oekofenc.load(False)

        if not servicestate.ok():
            llog.fatal(servicestate.report())

        self._booting = False
        self._on_connect()

        atexit.register(_mqttdisconnect)

        while servicestate.ok():
            time.sleep(interval)
            oekofenc.load()
            entitylist.report_entities()

        if not servicestate.ok():
            llog.error(servicestate.report())

        if not servicestate.oekofen_ok():
            hamqttc.publish_value(self._connecttopic, OFFLINE)


servicec = Service()