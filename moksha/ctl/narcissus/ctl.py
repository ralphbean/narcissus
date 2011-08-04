""" Functions for moksha-ctl """
import decorator
import subprocess
import os
import sys
import shutil
import psutil
import virtualenvcontext

# Local imports
import config
import colors as c
import utils


# load the narc config
ctl_config = config.load_config()

# Add moksha's src dir to the path so we can import it
sys.path.insert(0, ctl_config['moksha-src-dir'])

# Import moksha from its source directory
import moksha.ctl.core.ctl as moksha_ctl

# Override moksha config with narc config
moksha_ctl.ctl_config.update(ctl_config)

pid_files = ['paster.pid', 'orbited.pid', 'moksha-hub.pid']

PRETTY_PREFIX = "[ " + c.magenta("narc-ctl") + " ] "


@decorator.decorator
def _with_virtualenv(func, *args, **kwargs):
    with virtualenvcontext.VirtualenvContext(ctl_config['venv']):
        return func(*args, **kwargs)


@decorator.decorator
def _in_srcdir(func, *args, **kwargs):
    with utils.DirectoryContext(ctl_config['narc-src-dir']):
        return func(*args, **kwargs)

@decorator.decorator
def _with_moksha_faked(func, *args, **kwargs):
    ret = True

    # Do what moksha do, but don't change directory
    moksha_ctl.ctl_config['moksha-src-dir'] = ctl_config['narc-src-dir']

    # Call the function by name
    ret = getattr(moksha_ctl, func.__name__)(*args, **kwargs)

    moksha_ctl.ctl_config['moksha-src-dir'] = ctl_config['moksha-src-dir']

    # Go on with our narc business
    return func(*args, **kwargs) and ret
@decorator.decorator
def _with_moksha_first(func, *args, **kwargs):
    ret = True

    with utils.DirectoryContext(ctl_config['moksha-src-dir']):
        # Call the function by name
        ret = getattr(moksha_ctl, func.__name__)(*args, **kwargs)

    # Go on with our narc business
    return func(*args, **kwargs) and ret

@decorator.decorator
def _reporter(func, *args, **kwargs):
    PRETTY_PREFIX = "[ " + c.magenta("narc-ctl") + " ] "
    descriptor = ":".join([func.__name__] + [a for a in args if a])
    print PRETTY_PREFIX, "Running:", descriptor
    output = None
    try:
        output = func(*args, **kwargs)
        if not output:
            raise Exception
        print PRETTY_PREFIX, "[  " + c.green('OK') + "  ]", descriptor
    except Exception:
        print PRETTY_PREFIX, "[ " + c.red('FAIL') + " ]", descriptor
    return output


@_reporter
@_with_moksha_first
def bootstrap():
    """ Should only be run once.  First-time moksha setup. """
    print PRETTY_PREFIX, "Scratch that."
    print "Really, run './narc-ctl.py rebuild' to continue."
    return True


@_reporter
@_with_moksha_first
def rebuild():
    """ Completely destroy and rebuild the virtualenv. """
    return develop() and install_apps()


@_reporter
@_with_moksha_first
def install():
    """ Install moksha and all its dependencies. """
    return True


@_reporter
@_with_moksha_first
def install_hacks():
    """ Install dependencies with weird workarounds. """
    return True


@_reporter
@_with_moksha_first
def install_apps():
    """ Install *all* the moksha `apps`. """
    return True


@_reporter
@_with_moksha_first
def install_app(app):
    """ Install a particular app.  $ fab install_app:metrics """
    return True


@_reporter
@_with_moksha_first
def link_qpid_libs():
    """ Link qpid and mllib in from the system site-packages. """
    return True


@_reporter
@_with_moksha_faked
def start(service=None):
    """ Start paster, orbited, and moksha-hub. """
    return True


@_reporter
@_with_moksha_faked
def stop(service=None):
    """ Stop paster, orbited, and moksha-hub.  """
    return True


@_reporter
@_with_moksha_first
@_with_virtualenv
@_in_srcdir
def develop():
    """ `python setup.py develop` """
    ret = True
    ret = ret and not os.system('%s setup.py develop' % sys.executable)
#    ret = ret and not os.system('%s setup.py install' % sys.executable)
    return ret


@_reporter
@_with_moksha_faked
def restart():
    """ Stop, `python setup.py develop`, start.  """
    return True


@_with_moksha_faked
def logs():
    """ Watch colorized logs of paster, orbited, and moksha-hub """
    return True


# --
# Below here follows the *giant* 'wtf' block.  Add things to it as necessary.
# --

WTF_PREFIX = PRETTY_PREFIX + "[" + c.magenta('wtf') + "]"


def _wtfwin(msg):
    print WTF_PREFIX, "[  " + c.green('OK') + "  ]", msg


def _wtffail(msg):
    print WTF_PREFIX, "[ " + c.red('FAIL') + " ]", msg


@_with_moksha_faked
@_in_srcdir
def wtf():
    """ Debug a busted moksha environment. """
    wtfwin, wtffail = _wtfwin, _wtffail

    wtfwin('narc for the win')

