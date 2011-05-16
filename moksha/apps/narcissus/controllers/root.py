from tg import expose, validate, tmpl_context, redirect
from moksha.lib.base import Controller

from moksha.apps.narcissus.decorators import (
    with_moksha_socket,
    with_ui_theme,
    with_menu
)
import moksha.apps.narcissus.consumers
import moksha.utils

# TODO -- this should be moved to its own controller
import tw2.rrd
import tw2.core

import docutils.examples
import datetime
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

# TODO -- this should be moved to its own controller
def get_rrd_filenames(category):
    basedir = moksha.apps.narcissus.consumers.rrd_dir + '/' + category + '/'
    files = os.listdir(basedir)
    return [basedir + f for f in files]

class NarcissusController(Controller):

    @expose()
    def index(self, *args, **kw):
        redirect('/map')

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def countries(self, *args, **kw):
        tmpl_context.widget = moksha.utils.get_widget('narc_plot')(
            topic='http_counts_country')
        return dict(options={})

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def filenames(self, *args, **kw):
        tmpl_context.widget = moksha.utils.get_widget('narc_plot')(
            topic='http_counts_filename')
        return dict(options={})

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def map(self, *args, **kw):
        tmpl_context.widget = moksha.utils.get_widget('narc_map')
        return dict(options={})

    @expose('mako:moksha.apps.narcissus.templates.about')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def about(self, *args, **kw):
        tmpl_context.readme = readme_as_html()
        return dict(option={})

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def history(self, category, **kw):
        """ Static history graphs. """

        # TODO -- get these categories from a tg config
        if category not in ['country', 'filename']:
            redirect('/history/filename')

        tmpl_context.widget = tw2.rrd.RRDJitAreaChart(
            id='some_id',
            rrd_filenames=get_rrd_filenames(category),
            timedelta=datetime.timedelta(hours=1),
            width="900px",
            height="700px",
            offset=0,
            showAggregates=False,
            showLabels=False,
            Label = {
                'size': 15,
                'family': 'Arial',
                'color': 'white'
            },
            Tips = {
                'enable': True,
                'onShow' : tw2.core.JSSymbol(src="""
                (function(tip, elem) {
                    tip.innerHTML = "<b>" + elem.name + "</b>: " + elem.value +
                                        " hits per second.";
                })""")
            }
        )

        return dict(options={})

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def summary(self, category, **kw):
        # TODO -- get these categories from a tg config
        if category not in ['country', 'filename']:
            redirect('/summary/filename')

        tmpl_context.widget = tw2.rrd.RRDProtoBarChart(
            id='some_id',
            rrd_filenames=get_rrd_filenames(category),
            timedelta=datetime.timedelta(hours=2),
            p_height=700,
            p_width=900,
        )
        return dict(options={})

    # TODO -- this guy is really broken.  Don't use him.  :)
    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def stream(self, category, **kw):
        # TODO -- get these categories from a tg config
        if category not in ['country', 'filename']:
            redirect('/stream/filename')

        tmpl_context.widget = tw2.rrd.RRDStreamGraph(
            id='some_id',
            rrd_filenames=get_rrd_filenames(category),
            timedelta=datetime.timedelta(hours=2),
            p_height=700,
            p_width=900,
        )
        return dict(options={})

