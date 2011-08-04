from tg import expose, validate, tmpl_context, redirect, session
from moksha.lib.base import Controller

from moksha.apps.narcissus.decorators import (
    with_moksha_socket,
    with_ui_theme,
    with_menu
)
from moksha.apps.narcissus.controllers.api import APIController
from moksha.apps.narcissus.controllers.chart import ChartController

import moksha.utils

import docutils.examples
import os

import logging
log = logging.getLogger(__name__)

def readme_as_html():
    """ Ridiculous """
    root = '/'.join(__file__.split('/')[:-4])
    fname = root + '/README.rst'
    with open(fname, 'r') as f:
        readme = f.read()
        readme = readme.split('.. split here')[1]
        return docutils.examples.html_body(unicode(readme))

class NarcissusController(Controller):
    """ Main controller """

    # Mounting sub-controllers
    api = APIController()
    chart = ChartController()

    # Constants

    @expose()
    def index(self, *args, **kw):
        redirect('/map')

    @expose('mako:moksha.apps.narcissus.templates.widgets')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def countries(self, *args, **kw):
        tmpl_context.widgets = [
            moksha.utils.get_widget('narc_plot')(topic='http_counts_country'),
        ]
        return dict()

    @expose('mako:moksha.apps.narcissus.templates.widgets')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def filenames(self, *args, **kw):
        tmpl_context.widgets = [
            moksha.utils.get_widget('narc_plot')(topic='http_counts_filename'),
        ]
        return dict()

    @expose('mako:moksha.apps.narcissus.templates.widgets')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def map(self, *args, **kw):
        tmpl_context.widgets = [
            moksha.utils.get_widget('narc_map'),
        ]
        return dict()

    @expose('mako:moksha.apps.narcissus.templates.widgets')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def graph(self, *args, **kw):
        tmpl_context.widgets = [
            moksha.utils.get_widget('narc_graph'),
        ]
        return dict()

    @expose('mako:moksha.apps.narcissus.templates.about')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def about(self, *args, **kw):
        tmpl_context.readme = readme_as_html()
        return dict(option={})
