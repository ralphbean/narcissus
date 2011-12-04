""" Loading moksha-ctl config from file (and the defaults!) """

import os
import sys
import ConfigParser

EXAMPLE_CTL_CONF = """
# An example ~/.moksha/ctl.conf could look like this
[narc]
venv = fancy-narc
narc-src-dir = /home/user/devel/narc
moksha-src-dir = /home/user/devel/moksha
"""

def load_config(fname="~/.moksha/ctl.conf"):
    """ Load a config file into a dictionary and return it """

    # Defaults
    config_d = {
        'venv': 'narc',
        'apps-dir': 'moksha/apps',
        'narc-src-dir': os.getcwd(),
        'moksha-src-dir': os.getcwd() + '/../moksha'
    }

    config = ConfigParser.ConfigParser()

    fname = os.path.expanduser(fname)
    if not os.path.exists(fname):
        print "No such file '%s'" % fname
        print EXAMPLE_CTL_CONF
        sys.exit(1)

    with open(fname) as f:
        config.readfp(f)

    if not config.has_section('narc'):
        print "'%s' has no [narc] section" % fname
        print EXAMPLE_CTL_CONF
        sys.exit(1)

    # Extract all defined fields
    for key in ['moksha-src-dir', 'narc-src-dir', 'venv', 'apps-dir']:
        if config.has_option('narc', key):
            config_d[key] = config.get('narc', key)

    return config_d
