import time
import datetime
import json
import getopt
import sys
import logging
import logging.config

import parse
import config
import entitylist
import hamqtt
import oekofen

from const import (
    DAEMON,
    INTERVAL,
    LIST,
    LOGGING,
)

options = "plhc:"
longoptions = ["list", "help", "config="]

configfile = None

logging.config.dictConfig(LOGGING)
logger = logging.getLogger("default")

def _help():
    print("okofenmqtt options:")
    print("  -c <file> | --config <file>: configuration file")
    print("  -l | --list: list all available entities.")
    print("  -h | --help: print this help")
    print("You must specify a configuration file")
    exit()

def _handleOptions():
    global configfile
    try:
        arguments, values = getopt.getopt(sys.argv[1:], options, longoptions)
    
        for opt, val in arguments:
            if opt in ["-l", "--list"]:
                config.set(LIST, True)
                config.set(DAEMON, False)
                continue

            if opt in ["-c", "--config"]:
                configfile = val;
                continue
                
            if opt in ["-h", "--help"]:
                _help()
    
    except getopt.error as err:
        print (str(err))
        _help()

""" Main program """
def main():
    _handleOptions()
     
    if configfile is None:
        logger.error("No configuration file specified.")
        _help()
        
    config.load(configfile)
    config.cprint()

    if config.get(DAEMON):      
        logger.info("starting process")
        hamqtt.connect()
        
    interval = config.get(INTERVAL)

    """ This is temporary. We read a file, this should come from a call
    """
    while 1:
        ts = datetime.datetime.now().timestamp()
        fdata = oekofen.load()
        
        if not fdata is None:
            data = json.loads(fdata)
            parse.parser(data)
            
            if config.get(LIST): 
                entitylist.dump()

        nts = datetime.datetime.now().timestamp()
        waittime = max(1, interval - (nts - ts))
        
        time.sleep(waittime)
        
    logger.info("Exiting process")

if __name__ == "__main__":
    main()
