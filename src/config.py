from operator import truediv
import re
import yaml
import collections.abc
import copy
import llog

from const import (
    CLIENTID,
    COMPONENT,
    DEVICE,
    HOST,
    INTERVAL,
    JSONPORT,
    JSONPWD,
    LOGGER,
    MONITOR,
    MQTT,
    MQTTDEBUG,
    MQTTHOST,
    MQTTPORT,
    OEKOFEN,
)

_defaultconfig = {
    CLIENTID: "hamok",
    LOGGER: "default",
    MQTT: {
        MQTTPORT: 1883
    },
    OEKOFEN: {
        HOST: None,
        JSONPORT: None,
        JSONPWD: None,
    },
    MONITOR: {},
    INTERVAL: 60,
    DEVICE: "Oekofen",
    MQTTDEBUG: False,
}

_config = {}

def set(key: str, val):
    _config[key] = val

def get(key: str):
    return _config[key]

def load(filename, interactive):
    with open(filename) as file:
        cfg = yaml.full_load(file)

    update(_config, cfg)
    validate(interactive)

def cprint():
    temp = copy.deepcopy(_config)

    internals = list(filter( lambda x: x[0] == '_', temp.keys() ))
    for k in internals:
        del temp[k]
    dump = yaml.dump(temp)
    print(dump)

def update(d, u):
    for k, v in u.items():
        if v is None:
            d[k] = None
        if isinstance(v, collections.abc.Mapping):
            r = update(d.get(k, {}), v)
            d[k] = r
        else:
            d[k] = v
    return d

def normalize(s: str):
    rs = re.sub(r"\W", '_', s)
    return rs.lower()

def validate(interactive):
    fatal = False

    if not interactive:
        llog.changeLogger(_config.get(LOGGER))

    if _config[MQTT].get(MQTTHOST, None) is None:
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
        _config[INTERVAL] = _defaultconfig[INTERVAL]
    elif _config[INTERVAL] < 1 or _config[INTERVAL] > 86400:
        llog.error("Configuration of 'interval' must be between 0 and 86400. Using default value.")
        _config[INTERVAL] = _defaultconfig[INTERVAL]

    if len(_config[DEVICE]) == 0:
        llog.error("The device name may not be empty. Using default value.")
        _config[DEVICE] = _defaultconfig[DEVICE]
    _config[COMPONENT] = normalize(_config[DEVICE])

    c = _config[CLIENTID]
    l = len(c)
    if l > 0 and l < 23:
        vc = ascii(c).replace("'", "")
        if c != vc:
            llog.error("The client id should only contain alphanumeric characters. Using default value")
            _config[CLIENTID] = _defaultconfig[CLIENTID]
    else:
        llog.error("The clientid should contain between 1 and 23 alphanumeric characters. Using default value.")
        _config[CLIENTID] = _defaultconfig[CLIENTID]

    if fatal:
        llog.fatal(f"Configuration file is inconsistent. See previous errors.")


update( _config, _defaultconfig)