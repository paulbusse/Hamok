import re
import urllib.request
import json

import entitylist
import entity
import config
import llog

from jobs import jobhandler
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


    def load(self, on_success, on_failure):

        def oekofen_load(on_success, on_failure):
            try:
                res = urllib.request.urlopen(self._url + 'all?')
                rdata = res.read()
                jdata = json.loads(rdata.decode('latin-1'))
                if jdata:
                    self._parser(jdata)
                if on_success:
                    on_success()

            except Exception as e:
                llog.error(f"Loading info from Ökofen failed: {e}.")
                if on_failure:
                    on_failure()

        jobhandler.schedule({
                CALLBACK: oekofen_load,
                ARGUMENTS: [on_success, on_failure]
            })



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

        if ent.enabled:
            ent.set_okfval(data[VAL])


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


    def _parser(self, data: dict) -> dict:
        for key, val in data.items():
            self._parse_subsystem(key, val)

oekofenc = Oekofen()