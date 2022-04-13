import atexit
import time

import entitylist
import config
import llog

from oekofen import oekofenc
from hamqtt import hamqttc
from const import COMPONENT, INTERVAL, OFFLINE, ONLINE

def _mqttdisconnect():
    hamqttc.disconnect()

class Service:
    def __init__(self):
        self._failures = 0
        self._connecttopic = None
        self._firstrun = True

    @property
    def connecttopic(self):
        return self._connecttopic

    def configure(self):
        component = config.get(COMPONENT)
        self._connecttopic = f"hamok/{component}/connection"

        hamqttc.configure()
        oekofenc.configure()

        hamqttc.connect()
        atexit.register(_mqttdisconnect)


    def run(self):

        def on_success():
            self._failures = 0
            if self._firstrun:
                hamqttc.publish_value(self._connecttopic, ONLINE)
                entitylist.create_entities()
                hamqttc.subscribe()
                self._firstrun = False


        def on_failure():
            self._failures += 1

        interval = config.get(INTERVAL)

        while self._failures < 5: #FIXME make this configurable
            oekofenc.load(on_success, on_failure)
            time.sleep(interval)

        if self._failures >= 5:
            hamqttc.publish_value(self._connecttopic, OFFLINE)
            llog.fatal("Pellematic could not be reached 5 times.")


servicec = Service()