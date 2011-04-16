from tg import expose, validate, tmpl_context
from moksha.lib.base import Controller

import moksha.utils

from moksha.widgets.narcissus.widgets import NarcissusMapWidget

class NarcissusController(Controller):

    @expose('mako:moksha.apps.narcissus.templates.index')
    def index(self, *args, **kw):
        tmpl_context.widget = NarcissusMapWidget
        tmpl_context.moksha_socket = moksha.utils.get_widget('moksha_socket')
        return dict(options={})
