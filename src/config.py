from sre_constants import IN
import yaml
import collections.abc
import copy
import llog

from const import (
    CLIENTID,
    DAEMON,
    DEFAULTCONFIG,
    DEVICE,
    HOST,
    INTERVAL,
    JSONPORT,
    JSONPWD,
    LIST,
    LOGGER,
    MONITOR,
    MQTT,
    MQTTHOST,
    OEKOFEN,
    PRINT,
)

_config = DEFAULTCONFIG

def set(key: str, val):
    _config[key] = val

def get(key: str):
    return _config[key]

def load(filename):
    with open(filename) as file:
        cfg = yaml.full_load(file)
    
    update(_config, cfg)
    validate()
        
def cprint():
    temp = copy.deepcopy(_config)
    del temp[DAEMON]
    del temp[LIST]
    del temp[PRINT]
    dump = yaml.dump(temp)
    print(dump)

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def validate():
    fatal = False
    if _config[MQTT][MQTTHOST] is None:
        llog.error("No MQTT broker specified.")
        fatal = True
    
    if _config[OEKOFEN][HOST] is None:
        llog.error("The host of the Ökofen system is not specified.")
        fatal = True

    if _config[OEKOFEN][JSONPWD] is None:
        llog.error("The JSON password of the Ökofen system is not specified.")
        fatal = True

    if _config[OEKOFEN][JSONPORT] is None:
        llog.error("The JSON port of the Ökofen system is not specified.")
        fatal = True
    
    if len(_config[MONITOR]) == 0:
        llog.error("You must specify at least one value to monitor.")
        fatal = True

    if not isinstance(_config[INTERVAL], int):
        llog.error("Configuration of 'interval' does not contain integer. Using default value.")
        _config[INTERVAL] = DEFAULTCONFIG[INTERVAL]
    elif _config[INTERVAL] < 1 or _config[INTERVAL] > 86400:
        llog.error("Configuration of 'interval' must be between 0 and 86400. Using default value.")
        _config[INTERVAL] = DEFAULTCONFIG[INTERVAL]
        
    if len(_config[DEVICE]) == 0:
        llog.error("The device name may not be empty. Using default value.")
        _config[DEVICE] = DEFAULTCONFIG[DEVICE]
    
    c = _config[CLIENTID]
    l = len(c)
    if l > 0 and l < 23:
        vc = ascii(c).replace("'", "")
        if c == vc:
            llog.error("The clientid should contain between 1 and 23 alphanumeric characters. Using default value.")
            _config[CLIENTID] = DEFAULTCONFIG[CLIENTID]
    else:
        llog.error("The clientid should contain between 1 and 23 alphanumeric characters. Using default value.")
        _config[CLIENTID] = DEFAULTCONFIG[CLIENTID]
    
    llog.changeLogger(_config[LOGGER])
                
    if fatal:
        exit()