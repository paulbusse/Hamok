import re
import urllib.request
import json
import config
import llog
from jobs import jobhandler

from const import (
    CALLBACK,
    ARGUMENTS,
    OEKOFEN,
    HOST,
    JSONPORT,
    JSONPWD
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


    def load(self):
        try:
            res = urllib.request.urlopen(self._url + 'all?')
            rdata = res.read()
            jdata = json.loads(rdata.decode('latin-1'))
        except Exception as e:
            llog.error(f"Loading info from Ökofen failed: {e}")
            return None

        return jdata

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


oekofenc = Oekofen()