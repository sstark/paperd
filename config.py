
import yaml
import sys
import collections
import logging
import pprint

CONFIG_NAME = "paperd"
CONFIG_VERSION = "v1"

log = logging.getLogger("paperd.config")

class ConfMapping(collections.defaultdict):

    def __init__(self, *args, **kwargs):
        super().__init__(self.dfactory, *args, **kwargs)
        self.defaults = {
            "align": "left",
            "overflow": "resize",
            "color": 0,
            "background": 255
        }

    def __missing__(self, k):
        if self.default_factory is None:
            raise KeyError(k)
        else:
            ret = self[k] = self.default_factory(k)
            return ret

    def dfactory(self, k):
        log.debug("config value missing: %s", k)
        return self.defaults.get(k)

    def __str__(self):
        return pprint.pformat(dict(self.items()))

    def __repr__(self):
        # https://www.python.org/dev/peps/pep-3140/
        return self.__str__()

class ConfTree(ConfMapping):

    def __init__(self, filename, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.origconf = self.readConfigFile(filename)
        self.update(self.origconf)

    def readConfigFile(self, filename):

        with open(filename, 'r') as configFile:
            try:
                conf = yaml.full_load(configFile)[CONFIG_NAME][CONFIG_VERSION]
            except TypeError:
                log.exception("could not find configuration in %s" % filename)
                sys.exit(1)
            except yaml.parser.ParserError:
                log.exception("syntax error")
                sys.exit(1)
        return conf

def confMap_representer(dumper, data):
    return dumper.represent_dict(data.items())

def confMap_constructor(loader, node):
    return ConfMapping(loader.construct_pairs(node))

yaml.add_representer(ConfMapping, confMap_representer)
yaml.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,
                    confMap_constructor)
