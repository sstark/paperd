
import yaml
import sys
import collections
import logging

CONFIG_NAME = "paperd"
CONFIG_VERSION = "v1"

log = logging.getLogger("paperd.config")

class ConfMapping(collections.defaultdict):

    def __init__(self, *args, **kwargs):
        super().__init__(self.dfactory, *args, **kwargs)

    def __missing__(self, k):
        if self.default_factory is None:
            raise KeyError(k)
        else:
            ret = self[k] = self.default_factory(k)
            return ret

    def dfactory(self, k):
        log.debug("config value missing: %s", k)
        if k == "align":
            return "left"
        if k == "overflow":
            return "resize"
        if k == "color":
            return 0
        if k == "background":
            return 255
        return None

class ConfTree(ConfMapping):

    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.update(self.readConfigFile(filename))

    def readConfigFile(self, filename):

        with open(filename, 'r') as configFile:
            try:
                conf = yaml.load(configFile)[CONFIG_NAME][CONFIG_VERSION]
            except TypeError:
                log.exception("could not find configuration in %s" % filename)
                sys.exit(1)
            except yaml.parser.ParserError:
                log.exception("syntax error")
                sys.exit(1)
        return conf

def confMap_representer(dumper, data):
    return dumper.represent_dict(data.iteritems())

def confMap_constructor(loader, node):
    return ConfMapping(loader.construct_pairs(node))

yaml.add_representer(ConfMapping, confMap_representer)
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                    confMap_constructor)
