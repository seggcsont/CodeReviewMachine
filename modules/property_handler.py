import ConfigParser
import os
from gluon import current

property_handler = ConfigParser.ConfigParser()


def get_property(section, name):
    if not property_handler.sections():
        property_handler.read(os.path.join(current.request.folder,"config.properties"))
    try:
        return property_handler.get(section, name)
    except:
        return None
