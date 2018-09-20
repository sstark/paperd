#!/usr/bin/env python3

import yaml
from pprint import pprint
import sys
import argparse
import importlib
import os

__doc__ = """epaper display server

Receives images over http and renders them into predefined areas
on an epaper display.
"""
CONFIG_NAME = "paperd"
CONFIG_VERSION = "v1"
CONFIG_FILE = "paperd.yml"
OUTPUTS = ["pil", "epd2in9"]
DEFAULT_OUTPUT = "pil"

def readConfigFile(filename):
    with open(filename, 'r') as configFile:
        try:
            conf = yaml.safe_load(configFile)[CONFIG_NAME][CONFIG_VERSION]
        except KeyError:
            print("could not find configuration in %s" % filename)
            sys.exit(1)
        except yaml.parser.ParserError as e:
            print("syntax error")
            print(e)
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
    return vars(p.parse_args())

def loadOutputModule(drivername):
    try:
        if drivername.startswith("epd"):
            return importlib.import_module("show_epd")
        else:
            return importlib.import_module("show_"+drivername)
    except ModuleNotFoundError as e:
        print("could not load output module '%s' (or one of its dependencies)" % drivername)
        print(e)
        sys.exit(1)

args = readArgs()
pprint(args)

try:
    conf = readConfigFile(args["config"])
except FileNotFoundError as e:
    print("could not open configuration file")
    print(e)
    sys.exit(1)

outputDriver = DEFAULT_OUTPUT
if args["output"] is None:
    outputDriver = conf["output"]
else:
    outputDriver = args["output"]

out = loadOutputModule(outputDriver)
rc = out.RenderContext(outputDriver)
rc.run()

pprint(conf)
