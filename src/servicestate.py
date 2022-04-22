import time

class ServiceState:
    def __init__(self) -> None:
        self._ft = 300 # FIXME [23] make the self._ft configurable """
        now = time.time()
        self._mqttfailure = now
        self._mqttsuccess = now
        self._oekofenfailure = now
        self._oekofensuccess = now


    def mqtt(self, val: bool):
        if val:
            self._mqttsuccess = time.time()
        else:
            self._mqttfailure = time.time()


    def oekofen(self, val: bool):
        if val:
            self._oekofensuccess = time.time()
        else:
            self._oekofenfailure = time.time()


    def ok(self) -> bool:
        return ((self._mqttfailure - self._mqttsuccess) <= self._ft) and ((self._oekofenfailure - self._oekofensuccess) <= self._ft)


    def mqtt_ok(self) -> bool:
        return (self._mqttfailure - self._mqttsuccess) <= self._ft


    def oekofen_ok(self) -> bool:
        return (self._oekofenfailure - self._oekofensuccess) <= self._ft


    def report(self) -> str:
        mqttdiff = self._mqttfailure - self._mqttsuccess
        okfdiff = self._oekofenfailure - self._oekofensuccess
        mqttstate = "GREEN" if mqttdiff <= 0 else "RED" if mqttdiff > self._ft else "AMBER"
        okfstate =  "GREEN" if okfdiff <= 0 else "RED" if okfdiff > self._ft else "AMBER"
        return f"Service state: MQTT: {mqttstate} - Oekofen: {okfstate}"

servicestate = ServiceState()