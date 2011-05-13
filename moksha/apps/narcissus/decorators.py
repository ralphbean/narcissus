from tg import tmpl_context
import moksha.utils
from tw2.slideymenu import MenuWidget
from tw2.jqplugins.ui import set_ui_theme_name

import decorator

def with_moksha_socket(f, *args, **kw):
    tmpl_context.moksha_socket = moksha.utils.get_widget('moksha_socket')
    return f(*args, **kw)

def with_menu(f, *args, **kw):
    tmpl_context.menu_widget = MenuWidget(
        id='awesome-menu',
        items=[
            {
                'label' : 'Map (live)',
                'href' : '/map',
            },{
                'label' : 'Files (live)',
                'href' : '/filenames',
            },{
                'label' : 'Countries (live)',
                'href' : '/countries',
            },{
                'label' : 'Files (summary)',
                'href' : '/summary/filename',
            },{
                'label' : 'Countries (summ)',
                'href' : '/summary/country',
            },{
                'label' : 'Files (history)',
                'href' : '/history/filename',
            },{
                'label' : 'Countries (hist)',
                'href' : '/history/country',
            },{
                'label' : 'Logs (live)',
                'href' : '/logs',
            },{
                'label' : 'About',
                'href' : '/about',
            }
        ])
    return f(*args, **kw)

def with_ui_theme(f, *args, **kw):
    set_ui_theme_name('hot-sneaks') # hell yes
    return f(*args, **kw)

with_moksha_socket = decorator.decorator(with_moksha_socket)
with_menu = decorator.decorator(with_menu)
with_ui_theme = decorator.decorator(with_ui_theme)
