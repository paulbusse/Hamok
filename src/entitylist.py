from entity import BaseEntity
from hamqtt import hamqttc

_entities = {}

def get(key: str) -> BaseEntity:
    if key in _entities.keys():
        return _entities[key]
    else:
        return None

def add(key: str, ent: BaseEntity) -> None:
    _entities[key] = ent

def dump():
    for key in _entities.keys():
        entitytype = _entities[key].hatype
        if _entities[key].enabled:
            enabled = 'enabled'
        else:
            enabled = 'disabled'
        print(f"{key} [{entitytype}/{enabled}]")


def dumpvals():
    for key in _entities.keys():
        print(f"{key}: {_entities[key].get_haval()}")


def create_entities():
    for ent in _entities.values():
        if ent.enabled:
            hamqttc.create_entity(ent)
            hamqttc.publish_value(ent.statetopic, ent.get_haval())