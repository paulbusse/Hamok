"""
These classes have 2 value attributes: value and jsonvalue.

okfval is set when we collect new info from the system. if the monitor
is enabled it is published on the MQTT topic.

haval is set when we retrieve a value from MQTT. That value is forwarded
to the heating system.

Internally we only maintain the HA value.
"""

import re
import config
import llog

from hamqtt import hamqttc
from oekofen import oekofenc
from jobs import jobhandler
from service import servicec

from const import (
    COMPONENT,
    DELAY,
    DEVICE,

    BINARYSENSOR,
    DEVICECLASS,
    MAXIMUM,
    MINIMUM,
    MONITOR,
    NUMBER,
    SELECT,
    SENSOR,
    SWITCH,

    FACTOR,
    FORMAT,
    TOPICROOT,
    UNIT,

    ONOFFFORMATS,
    ON,
    OFF,
)

class BaseEntity(object):
    """ Base class for all entities """

    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data):
        """ You cannot use any of the derived functions in this function """
        component = config.get(COMPONENT)
        device = config.get(DEVICE)
        monitors = config.get(MONITOR)

        if attribute[0:2] == "L_":
            _friendly = attribute[2:]
        else:
            _friendly = attribute

        en = component + "_" + systemname + "_" + _friendly
        en = config.normalize(en)

        self._hatype = entitytype
        self._id = device + "_" + systemlabel + "_" + attribute
        self._entityname = en
        self._oekofenname = systemlabel + "." + attribute
        self._value = None
        self._latestreport = 0
        self._latestvalue = None

        self._enabled = self._oekofenname in monitors.keys();
        monconf = monitors.get(self._oekofenname, None)

        if monconf is None:
            self._delay = 0
            self._device_class = None
        else:
            self._delay = monconf.get(DELAY, 0)
            self._device_class = monconf.get(DEVICECLASS, None)

    def __repr__(self):
        return self._entityname

    @property
    def name(self):
        return self._entityname

    @property
    def hatype(self):
        return self._hatype

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, e):
        self._enabled = e;

    @property
    def basetopic(self):
        component = config.get(COMPONENT)
        return TOPICROOT + self.hatype + "/" + component + "/" + self._entityname

    @property
    def createtopic(self):
        return self.basetopic + '/config'

    @property
    def statetopic(self):
        return self.basetopic + '/state'

    @property
    def cmdtopic(self):
        return None

    @property
    def okfname(self):
        return self._oekofenname

    @property
    def device_class(self):
        return None

    def set_okfval(self, v):
        self._value = v

    def get_haval(self):
        return self._value

    def report(self, now):
        v = self.get_haval();
        if self._latestvalue == v:
            return

        if self._latestreport + self._delay > now:
            llog.debug(f"{self.name} has changed but too early to report.")
            return

        hamqttc.publish_value(self.statetopic, v)
        self._latestreport = now
        self._latestvalue = v


    def control_data(self):
        device = config.get(DEVICE)
        return {
            '~': self.basetopic,
            'availability': [
                {'topic': servicec.connecttopic },
            ],
            'state_topic': self.statetopic,
            'device': {
                'manufacturer': 'Ökofen',
                'identifiers': ["123456789"], #FIXME: find real identifier
                'name': device,
                'sw_version': 'v4.00b', #FIXME: find this from system
            },
            'name': self._entityname,
            'unique_id': self._id,
        }


class BinarySensorEntity(BaseEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)

    @property
    def device_class(self):
        return self._device_class

    def set_okfval(self, v):
        hav = ON if v == 1 else OFF
        super().set_okfval(hav)

    def control_data(self):
        data = super().control_data()
        data['payload_on'] = ON
        data['payload_off'] = OFF
        if not self._device_class is None:
            data[DEVICECLASS] = self._device_class
        return data


class SelectSensorEntity(BaseEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)
        self._options = self._split(data[FORMAT])

    def set_okfval(self, v):
        iv = int(v)
        if iv < 0 or iv >= len(self._options):
            llog.info( f"{self._entityname}: option not available ({iv} out of {len(self._options)}). Ignored.")
            return
        super().set_okfval(self._options[int(v)])

    @property
    def options(self):
        return self._options

    def _split(self, format: str):
        a = re.split(r'[|:]', format)
        return a[1::2]


class NumberSensorEntity(BaseEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)

        if UNIT in data.keys():
            self._unit = data[UNIT]
        else:
            self._unit = ""

        if FACTOR in data.keys():
            self._factor = data[FACTOR]
        else:
            self._factor = 1

        if self._unit == '%':
            self._min = 0
            self._max = 100
        elif self._unit == '°C':
            self._min = -50
            self._max = 1500
        elif MINIMUM in data.keys():
            self._min = int(data[MINIMUM]) * self._factor
            self._max = int(data[MAXIMUM]) * self._factor
        else:
            self._min = None
            self._max = None

    def get_haval(self):
        if self._value is not None:
            prec = 1 if self._factor < 1 else 0
            return f"{self._value:.{prec}f}"

    def set_okfval(self, v):
        fv = float(v) * self._factor
        if self._min is not None:
            if self._enabled and (fv < self._min or fv > self._max):
                llog.info(f'Ignoring value out of range({self._entityname}, {fv}).')
                return
        super().set_okfval(fv)

    def control_data(self):
        data = super().control_data()
        if self._unit:
            data['unit_of_measurement'] = self._unit
        if not self._device_class is None:
            data[DEVICECLASS] = self._device_class
        return data


class ReadWriteEntity(BaseEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)

    def set_haval(self, v):
        def do_set_haval(okfname, val, oldval):
            ret = oekofenc.publish_value(okfname, val)
            if ret:
                hamqttc.publish_value(self.statetopic, self.get_haval())
            else:
                self.set_okfval(oldval)

        if v != self._value:
            oldval = self.get_okfval()
            self._value = v
            jobhandler.schedule( do_set_haval, self._oekofenname, self.get_okfval(), oldval)

    def control_data(self):
        data = super().control_data()
        data['command_topic'] = '~/cmd'
        return data

    @property
    def cmdtopic(self):
        return self.basetopic + '/cmd'


class SwitchEntity(BinarySensorEntity, ReadWriteEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)

    def get_okfval(self):
        return 1 if self._value == ON else 0


class SelectEntity(SelectSensorEntity, ReadWriteEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)

    def get_okfval(self):
        return f"{self.options.index(self._value)}"

    def control_data(self):
        data = super().control_data()
        data['options'] = self._options
        return data


class NumberEntity(NumberSensorEntity, ReadWriteEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)



    def get_okfval(self):
        return f"{self._value / self._factor:.0f}"

    def set_haval(self, v):
        return super().set_haval(float(v))

    def control_data(self):
        data = super().control_data()
        if self._min:
            data['min'] = self._min
            data['max'] = self._max
        return data


def factory(subsysname, subsyslabel, entityname, data: dict):
    readonly = False
    binary = False
    select = False
    if entityname[0:2] == 'L_':
        readonly = True

    if FORMAT in data.keys():
        if data[FORMAT] in ONOFFFORMATS:
            binary = True
        else:
            select = True

    if readonly:
        if binary:
            ent = BinarySensorEntity(BINARYSENSOR, subsysname, entityname, subsyslabel,  data)
        elif select:
            ent = SelectSensorEntity(SENSOR, subsysname, entityname, subsyslabel, data)
        else:
            ent = NumberSensorEntity(SENSOR, subsysname, entityname, subsyslabel, data)
    else:
        if binary:
            ent = SwitchEntity(SWITCH, subsysname, entityname, subsyslabel, data)
        elif select:
            ent = SelectEntity(SELECT, subsysname, entityname, subsyslabel, data)
        else:
            ent = NumberEntity(NUMBER, subsysname, entityname, subsyslabel, data)

    return ent
