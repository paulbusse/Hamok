import time
import atexit
import getopt
import sys
import signal

import config
import entitylist
from hamqtt import hamqttc
from oekofen import oekofenc
from jobs import jobhandler

import llog

from const import (
    INTERVAL,
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


def _list():
    oekofenc.configure()
    oekofenc.load()
    entitylist.dump()
    exit()


def _print():
    config.cprint()
    exit()

def _service():

    oekofenc.configure()
    oekofenc.load()

    """ Set up the environment for the main loop """

    _set_sighandler()

    llog.info("starting process")
    atexit.register(_exitlog)

    hamqttc.connect()
    atexit.register(_mqttdisconnect)

    entitylist.create_entities()
    hamqttc.subscribe()

    interval = config.get(INTERVAL)

    """ We can now start the main loop """

    run = True # For future use!
    while run:
        time.sleep(interval)
        jobhandler.execute_alljob()


def _handleOptions():
    global configfile
    executor = _service
    try:
        arguments, values = getopt.getopt(sys.argv[1:], options, longoptions)

        for opt, val in arguments:
            if opt in ["-l", "--list"]:
                executor = _list
                continue

            if opt in ["-p", "--print"]:
                executor = _print
                continue

            if opt in ["-c", "--config"]:
                configfile = val;
                continue

            if opt in ["-h", "--help"]:
                _help()

    except getopt.error as err:
        print (str(err))
        _help()

    return executor

def _exitlog():
    llog.info("Exiting process")

def _mqttdisconnect():
    hamqttc.disconnect()

def _sighandler(signum, frame):
    name = signal.Signals(signum).name
    if signum in [
        signal.SIGHUP,
        signal.SIGINT,
        signal.SIGQUIT,
        signal.SIGTERM,
        signal.SIGPWR,
    ]:
        llog.info(f"Received signal {name}({signum}). Exiting")
        exit()
    else:
        llog.debug(f"Received signal {name}({signum}). Ignoring")


def _set_sighandler():
    for s in signal.Signals:
        v = signal.Signals(s).value
        try:
            signal.signal(s, _sighandler)
        except OSError as e:
            pass


""" Main program """
def main():
    executor = _handleOptions()

    if configfile is None:
        llog.error("No configuration file specified.")
        _help()

    config.load(configfile)

    executor()


if __name__ == "__main__":
    main()
