from entity import BaseEntity

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
        print("{} [{}/{}]".format(key, entitytype, enabled))