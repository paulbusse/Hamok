from distutils.command.build import build
import urllib.request
import config
import logging

logger = logging.getLogger("default")

from const import (
    OEKOFEN,
    HOST,
    JSONPORT,
    JSONPWD
)

url = None

def buildURL():
    cfg = config.get(OEKOFEN)
    host = cfg[HOST]
    port = cfg[JSONPORT]
    pwd = cfg[JSONPWD]
    url = 'http://' + host + ':' + str(port) + '/' + pwd + '/'
    return url

def load():
    global url
    if url is None:
        url = buildURL()
    
    try:
        with urllib.request.urlopen(url + 'all?') as response:
            html = response.read()
        return html.decode('iso-8859-1')
    except Exception as e:
        logger.error("Failed to get the information from the Ökofen system. Retrying.")
        return None
