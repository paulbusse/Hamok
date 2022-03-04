"""
These classes have 2 value attributes: value and jsonvalue.

okfval is set when we collect new info from the system. if the monitor
is enabled it is published on the MQTT topic.

haval is set when we retrieve a value from MQTT. That value is forwarded
to the heating system.

Internally we only maintain a variable value.
"""

import re
import logging

import config
from hamqtt import publish_value

from const import (
    COMPONENT,
    
    BINARYSENSOR,
    MAXIMUM,
    MINIMUM,
    NUMBER,
    SELECT,
    SENSOR,
    SWITCH,
    
    FACTOR,
    FORMAT,
    TOPICROOT,
    UNIT,
    
    ONOFFFORMATS,
)

logger = logging.getLogger("default")

""" HA switch statuses"""
ON = 'ON'
OFF = 'OFF'

class BaseEntity(object):
    """ Base class for all entities """
    
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data):
        """ You cannot use any of the derived functions in this function """
        component = config.get(COMPONENT)
        
        if attribute[0:2] == "L_":
            _friendly = attribute[2:]
        else:
            _friendly = attribute
        
        en = component + "_" + systemname + "_" + _friendly
        en = en.lower()
        en = re.sub(r"\W", '_', en)
        
        self._hatype = entitytype
        self._id = component + "_" + systemlabel + "_" + attribute
        self._entityname = en
        self._oekofenname = systemlabel + "." + attribute
        self._enabled = False
        self._value = None
        
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
        return TOPICROOT + self.hatype + "/" + component + "/" + self._id
        
    @property
    def createtopic(self):
        return self.basetopic + '/config'
    
    @property
    def statetopic(self):
        return self.basetopic + '/state'
    
    def get_okfval(self):
        logger.error("abstract function 'get_okfval' called.")
    
    def set_okfval(self, v):
        if not self._value or v != self._value:
            self._value = v
            publish_value(self)
        
    def get_haval(self):
        return self._value
        
    def set_haval(self, v):
        logger.error("abstract function 'set_haval' called.")
    
    def control_data(self):
        component = config.get(COMPONENT)
        return {
            '~': self.basetopic,
            'state_topic': self.statetopic,
            'device': {
                'manufacturer': 'Ökofen',
                'identifiers': ["123456789"], #TODO: find real identifier
                'name': config.get(COMPONENT),
                'sw_version': 'v4.00b', #TODO: find this from system
            },
            # device_class: skipped for now
            'name': self._entityname,
            'unique_id': self._id,
            'value_template': '{{value_json.val}}'
        }
        

class BinarySensorEntity(BaseEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)
    
    def set_okfval(self, v):
        hav = ON if v == 1 else OFF
        super().set_okfval(hav)

    def control_data(self):
        data = super().control_data()
        data['payload_on'] = ON
        data['payload_off'] = OFF
        return data
            

class SelectSensorEntity(BaseEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):    
        super().__init__(entitytype, systemname, attribute, systemlabel, data)
        self._options = self._split(data[FORMAT])
    
    def set_okfval(self, v):
        super().set_okfval(self._options[v])
    
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
            

    def set_okfval(self, v):
        super().set_okfval(v * self._factor)
    
    def control_data(self):
        data = super().control_data()
        if self._unit:
            data['unit_of_measurement'] = self._unit
        return data
     
        
class ReadWriteEntity(BaseEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):    
        super().__init__(entitytype, systemname, attribute, systemlabel, data)
    
    def set_haval(self, v):
        self._value = v
    
    def control_data(self):
        data = super().control_data()
        data['command_topic'] = '~/cmd'
        return data
    

class SwitchEntity(BinarySensorEntity, ReadWriteEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)

    def get_okfval(self):
        return 1 if self._value == ON else 0


class SelectEntity(SelectSensorEntity, ReadWriteEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)

    def get_okfval(self):
        return self.options.index(self._value)
    
    def control_data(self):
        data = super().control_data()
        data['options'] = self._options
        return data
    

class NumberEntity(NumberSensorEntity, ReadWriteEntity):
    def __init__(self, entitytype: str, systemname: str, attribute: str, systemlabel: str, data ):
        super().__init__(entitytype, systemname, attribute, systemlabel, data)
        
        if MINIMUM in data.keys():
            self._min = data[MINIMUM] * self._factor
            self._max = data[MAXIMUM] * self._factor
        else:
            self._min = ""
            self._max = ""

    def get_okfval(self):
        return self._value / self._factor
    
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