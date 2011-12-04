from tg import tmpl_context
import moksha.utils
from moksha.widgets.narcissus.widgets import NarcissusMenu
from tw2.jqplugins.ui import set_ui_theme_name

import decorator

def with_moksha_socket(f, *args, **kw):
    tmpl_context.moksha_socket = moksha.utils.get_widget('moksha_socket')
    return f(*args, **kw)

def with_menu(f, *args, **kw):
    tmpl_context.menu_widget = NarcissusMenu
    return f(*args, **kw)

def with_ui_theme(f, *args, **kw):
    set_ui_theme_name('hot-sneaks') # hell yes
    return f(*args, **kw)

with_moksha_socket = decorator.decorator(with_moksha_socket)
with_menu = decorator.decorator(with_menu)
with_ui_theme = decorator.decorator(with_ui_theme)
