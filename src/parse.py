import entity
import entitylist
import hamqtt
import config

from const import DAEMON, MONITOR, NAME, VAL

def _parseEntity(systemlabel: str, subname, entityname: str, data: dict):
    """
    Parse the system part of data
    We are actually only interested in the ambient temperature
    """
    
    daemon = config.get(DAEMON)
    entityKey = systemlabel + "." + entityname
    ent = entitylist.get(entityKey)
    if ent is None:
        ent = entity.factory(subname, systemlabel, entityname, data)
        
        ent.enabled = entityKey in config.get(MONITOR)
        
        entitylist.add(entityKey, ent)
        
        if ent.enabled and daemon:
            hamqtt.create_entity(ent)
            
    if ent.enabled and daemon:
        ent.set_okfval(data[VAL])
 
        
def _parseSubsystem(subname: str, data: dict):
    """ Parse the subsystem """
    
    if NAME in data.keys():
        name = data[NAME][VAL]
    else:
        name = subname
        
    for key, val in data.items():
        if key == NAME:
            continue
        if type(val) is dict:
            _parseEntity(subname, name, key, val)

    
def parser(data: dict) -> dict:
    for key, val in data.items():
        _parseSubsystem(key, val)