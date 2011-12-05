#!/usr/bin/env python
""" This command is used to manage the narc development configuration.

Example:
    $ ./narc-ctl.py bootstrap
    $ ./narc-ctl.py rebuild
    $ ./narc-ctl.py start
    $ ./narc-ctl.py wtf
    $ tail -f logs/paster.log | ccze
    $ tail -f [moksha-source-location]/logs/moksha-hub.log | ccze

Passing arguments:
    You can also pass arguments to particular commands like start, restart, and
    stop, and install_app.

    $ ./narc-ctl.py restart:moksha-hub

Virtual Environments:
    Virtualenvs are managed for you by way of virtualenvwrapper.  Check in
    ~/.virtualenvs for the actual directory structure.  You can also specify
    what environment to use with the -E or --environment=some_env options."""

import optparse
import types
import sys

""" Loading moksha-ctl config from file (and the defaults!) """

import os
import sys
import ConfigParser

EXAMPLE_CTL_CONF = """
# An example ~/.moksha/ctl.conf could look like this
[narc]
venv = narc
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

# load the narc config
ctl_config = load_config()

# Add moksha's src dir to the path so we can import it
sys.path.insert(0, ctl_config['moksha-src-dir'])

import narcissus.ctl.ctl as ctl

usage = "usage: %prog [options] command1 [command2, command3, ...]"
usage += "\n\n" + __doc__ + "\n\nCommands:\n"
cmd_usage_template = "{cmd:>15}  {help}"

if __name__ == '__main__':
    # First, extract all non-hidden functions from the core module
    funcs = [f for f in dir(ctl) if (
        f[0] != '_' and isinstance(getattr(ctl, f), types.FunctionType)
    )]

    # Construct a nice usage string
    usage = usage + '\n'.join([
        cmd_usage_template.format(
            cmd=func, help=getattr(ctl, func).__doc__)
        for func in funcs
    ])

    parser = optparse.OptionParser(usage=usage)
    parser.add_option('-E', '--environment', dest='venv', default=None,
                      help='name of the virtualenv to use')

    opts, args = parser.parse_args()
    arguments = []
    for arg in args:
        items = arg.split(':')
        arguments.append({'cmd':items[0], 'args':items[1:]})

    failed = [arg['cmd'] for arg in arguments if not arg['cmd'] in funcs]
    if failed:
        for fail in failed:
            print " * %s is not a command" % fail
        print
        parser.print_usage()
        sys.exit(0)

    if opts.venv:
        ctl.moksha_ctl.ctl_config['venv'] = ctl.ctl_config['venv'] = opts.venv

    # Actually execute the commands
    for arg in arguments:
        getattr(ctl, arg['cmd'])(*arg['args'])
