import time

import getopt
import sys

import parse
import config
import entitylist
from hamqtt import hamqttc
from oekofen import oekofenc
from jobs import jobhandler

import llog

from const import (
    INTERVAL,
    LIST,
    PRINT,
)

options = "c:hlp"
longoptions = ["config=", "help", "list", "print"]

configfile = None

def _help():
    print("okofenmqtt options:")
    print("  -c <file> | --config <file>: configuration file")
    print("  -l | --list: list all available entities.")
    print("  -p | --print: print the current configuration")
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
                continue

            if opt in ["-p", "--print"]:
                config.set(PRINT, True)
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
        llog.error("No configuration file specified.")
        _help()

    config.load(configfile)

    if config.get(PRINT):
        config.cprint()
        exit()

    oekofenc.configure()
    data = oekofenc.load()
    if data:
        parse.parser(data)
    else:
        llog.error("Could not retrieve information from Ökofen system.")
        exit()

    if config.get(LIST):
        entitylist.dump()
        exit()

    """ We can now start the main loop """

    """ Start threads """
    llog.info("starting process")

    hamqttc.connect()
    entitylist.create_entities()
    hamqttc.subscribe()

    interval = config.get(INTERVAL)

    run = True # For future use!
    while run:
        time.sleep(interval)
        jobhandler.execute_alljob()

    llog.info("Exiting process")

if __name__ == "__main__":
    main()
