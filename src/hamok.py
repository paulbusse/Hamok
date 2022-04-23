import atexit
import getopt
import sys
import signal

import config
from const import COMPONENT
import entitylist
import llog

from service import servicec
from oekofen import oekofenc
from jobs import jobhandler



options = "c:f:hlp"
longoptions = ["config=", "file=", "help", "list", "print"]

configfile = None
parsefile = None

def _help():
    print("hamok options:")
    print("  -c <file> | --config <file>: configuration file")
    print("  -f <file> | --file <file>: parse file and exit")
    print("  -l | --list: list all available entities.")
    print("  -p | --print: print the current configuration")
    print("  -h | --help: print this help")
    print("You must specify a configuration file")
    exit()

def _file():
    global parsefile
    llog.changeLogger("devel")
    config.set(COMPONENT, "default")
    oekofenc.loadfile(parsefile)
    entitylist.dumpvals()

def _list():
    oekofenc.configure()
    oekofenc.load()
    jobhandler.wait()
    entitylist.dump()


def _print():
    config.cprint()
    exit()

def _service():

    servicec.configure()
    _set_sighandler()

    llog.info("starting process")
    atexit.register(_exitlog)

    servicec.run()


def _handleOptions():
    global configfile, parsefile
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
                configfile = val
                continue

            if opt in ["-f", "--file"]:
                parsefile = val
                executor = _file
                continue

            if opt in ["-h", "--help"]:
                _help()

    except getopt.error as err:
        print (str(err))
        _help()

    return executor


def _exitlog():
    llog.info("Exiting process")


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

    if executor != _file:
        if configfile is None :
            llog.error("No configuration file specified.")
            _help()

        config.load(configfile)

    executor()


if __name__ == "__main__":
    main()
