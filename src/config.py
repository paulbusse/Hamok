import yaml
import collections.abc
import copy
from llog import changeLogger

from const import (
    DAEMON,
    LIST,
    DEFAULTCONFIG,
    PRINT,
    LOGGER,
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
    validateLogger()
        
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

def validateLogger():
    logmode = get(LOGGER)
    changeLogger(logmode)