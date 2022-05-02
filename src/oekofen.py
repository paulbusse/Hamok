import re
import urllib.request
import json

import entitylist
import entity
import config
import llog

from jobs import jobhandler
from servicestate import servicestate
from const import (
    ARGUMENTS,
    CALLBACK,
    HOST,
    JSONPORT,
    JSONPWD,
    MONITOR,
    NAME,
    OEKOFEN,
    VAL,
)

class Oekofen:

    def __init__(self):
        self._url = None

    def configure(self):
        cfg = config.get(OEKOFEN)
        host = cfg[HOST]
        port = cfg[JSONPORT]
        pwd = cfg[JSONPWD]
        self._url = 'http://' + host + ':' + str(port) + '/' + pwd + '/'


    def load(self, launchjob = True):

        def oekofen_load():
            try:
                res = urllib.request.urlopen(self._url + 'all?')
                rdata = res.read()
                jdata = json.loads(rdata.decode('latin-1'))
                if jdata:
                    self._parser(jdata)
                servicestate.oekofen(True)
                return True

            except Exception as e:
                llog.error(f"Loading info from Ökofen failed: {e}.")
                servicestate.oekofen(False)

            return False

        if launchjob:
            jobhandler.schedule({
                    CALLBACK: oekofen_load,
                    ARGUMENTS: []
                })
            return True
        else:
            return oekofen_load()

    def loadfile(self, file):
        try:
            f = open(file, "r")
        except Exception as e:
            llog.error(f"Could not open {file}: {e}")
            return

        jdata = json.load(f)
        if jdata:
            self._parser(jdata)


    def publish_value(self, okfname, val):
        try:
            res = urllib.request.urlopen(self._url + okfname + '=' + val)
            rdata = res.read().decode('latin-1')
            m = re.search( '(?<==)\w+', rdata)
            nval = m.group(0)

            if val == nval:
                llog.info(f"Setting {okfname} to {val}: success")
            return True

        except Exception as e:
            llog.info(f"Setting {okfname} to {val}: failed[{e}].")
            return False

    def _parse_entity(self, systemlabel: str, subname, entityname: str, data: dict):
        """
        Parse the system part of data
        We are actually only interested in the ambient temperature
        """

        entityKey = systemlabel + "." + entityname
        ent = entitylist.get(entityKey)
        if ent is None:
            ent = entity.factory(subname, systemlabel, entityname, data)
            ent.enabled = entityKey in config.get(MONITOR)
            entitylist.add(entityKey, ent)

        v = data[VAL]
        if v == "true":
            v = 1
        if v == "false":
            v = 0
        ent.set_okfval(v)


    def _parse_subsystem(self, subname: str, data: dict):
        """ Parse the subsystem """

        if NAME in data.keys():
            name = data[NAME][VAL]
        else:
            name = subname

        for key, val in data.items():
            if key == NAME:
                continue
            if type(val) is dict:
                self._parse_entity(subname, name, key, val)


    def _parser(self, data) -> None:
        if not data:
            return

        for key, val in data.items():
            if not key in ["forecast", "weather"]:
                self._parse_subsystem(key, val)

oekofenc = Oekofen()