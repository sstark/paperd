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

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("paperd")

def readConfigFile(filename):
    with open(filename, 'r') as configFile:
        try:
            conf = yaml.safe_load(configFile)[CONFIG_NAME][CONFIG_VERSION]
        except KeyError:
            log.exception("could not find configuration in %s" % filename)
            sys.exit(1)
        except yaml.parser.ParserError:
            log.exception("syntax error")
            sys.exit(1)
    return conf

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

try:
    conf = readConfigFile(args["config"])
except FileNotFoundError as e:
    log.error("could not open configuration file")
    log.error(e)
    sys.exit(1)

outputDriver = DEFAULT_OUTPUT
if args["output"] is None:
    outputDriver = conf["output"]
else:
    outputDriver = args["output"]

out = loadOutputModule(outputDriver)
rc = out.RenderContext(outputDriver, conf, args["scale"])
rc.run()

log.debug(conf)
