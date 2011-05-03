from tg import expose, validate, tmpl_context
from moksha.lib.base import Controller

import docutils.examples

import moksha.utils

import logging
log = logging.getLogger(__name__)


def readme_as_html():
    """ Ridiculous """
    log.info("readme as html")
    root = '/'.join(__file__.split('/')[:-4])
    log.info("readme as html", root)
    fname = root + '/README.rst'
    log.info("readme as html", fname)
    with open(fname, 'r') as f:
        readme = f.read()
        return docutils.examples.html_body(unicode(readme))


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

    @expose('mako:moksha.apps.narcissus.templates.about')
    def about(self, *args, **kw):
        tmpl_context.readme = readme_as_html()
        tmpl_context.moksha_socket = moksha.utils.get_widget('moksha_socket')
        return dict(option={})
