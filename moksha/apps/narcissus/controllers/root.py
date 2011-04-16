from tg import expose, validate, tmpl_context
from moksha.lib.base import Controller

import moksha.utils

class NarcissusController(Controller):
    @expose('mako:moksha.apps.narcissus.templates.index')
    def index(self, *args, **kw):
        tmpl_context.mapwidget = moksha.utils.get_widget('narc_map')
        tmpl_context.plotwidget = moksha.utils.get_widget('narc_plot')
        tmpl_context.moksha_socket = moksha.utils.get_widget('moksha_socket')
        return dict(options={})
    @expose('mako:moksha.apps.narcissus.templates.plot')
    def plot(self, *args, **kw):
        tmpl_context.plotwidget = moksha.utils.get_widget('narc_plot')
        tmpl_context.moksha_socket = moksha.utils.get_widget('moksha_socket')
        return dict(options={})
    @expose('mako:moksha.apps.narcissus.templates.map')
    def map(self, *args, **kw):
        tmpl_context.mapwidget = moksha.utils.get_widget('narc_map')
        tmpl_context.moksha_socket = moksha.utils.get_widget('moksha_socket')
        return dict(options={})
