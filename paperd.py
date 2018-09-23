#!/usr/bin/env python3

import yaml
import sys
import argparse
import importlib
import os
import logging

__doc__ = """epaper display server

Receives images over http and renders them into predefined areas
on an epaper display.
"""
CONFIG_NAME = "paperd"
CONFIG_VERSION = "v1"
CONFIG_FILE = "paperd.yml"
OUTPUTS = ["pil", "tk", "epd2in9"]
DEFAULT_OUTPUT = "pil"
DEFAULT_SCALE = 1
WEBSERVER_DEFAULT_HOSTNAME = "localhost"
WEBSERVER_DEFAULT_PORT = 2354

try:
    loglevel = os.environ["PAPERD_LOGLEVEL"]
except:
    loglevel = ""
if loglevel.lower() == "debug":
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.INFO)
log = logging.getLogger("paperd")

def readArgs():
    p = argparse.ArgumentParser(description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument('-c', '--config',
                   default=CONFIG_FILE,
                   help='path to yaml configuration file')
    p.add_argument('-o', '--output',
                   choices=OUTPUTS,
                   help='output driver (overrides value from config file)')
    p.add_argument('-s', '--scale',
                   default=DEFAULT_SCALE,
                   type=int,
                   help='scale up preview (e. g. for use on hidpi displays)')
    p.add_argument('-l', '--listen',
                   default=WEBSERVER_DEFAULT_HOSTNAME,
                   type=str,
                   help='address or hostname the webserver should listen on')
    p.add_argument('-p', '--port',
                   default=WEBSERVER_DEFAULT_PORT,
                   type=int,
                   help='port number the webserver should listen on')
    return vars(p.parse_args())

def loadOutputModule(drivername):
    try:
        if drivername.startswith("epd"):
            return importlib.import_module("show_epd")
        else:
            return importlib.import_module("show_"+drivername)
    except ModuleNotFoundError:
        log.exception("could not load output module '%s' (or one of its dependencies)" % drivername)
        sys.exit(1)

args = readArgs()
log.debug(args)
log.info("paperd - epaper display server")

import config
try:
    conf = config.ConfTree(args["config"])
except FileNotFoundError as e:
    log.error("could not open configuration file")
    log.error(e)
    sys.exit(1)

log.debug(conf)

outputDriver = DEFAULT_OUTPUT
if args["output"] is None:
    outputDriver = conf["output"]
else:
    outputDriver = args["output"]

conf["listen"] = (args["listen"], args["port"])

out = loadOutputModule(outputDriver)
rc = out.RenderContext(outputDriver, conf, args["scale"])
rc.run()
