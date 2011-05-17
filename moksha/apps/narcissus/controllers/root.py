from tg import expose, validate, tmpl_context, redirect, session
from moksha.lib.base import Controller

from moksha.apps.narcissus.decorators import (
    with_moksha_socket,
    with_ui_theme,
    with_menu
)
from moksha.apps.narcissus.controllers.api import APIController
import moksha.apps.narcissus.consumers
import moksha.widgets.narcissus.widgets as widgets
import moksha.utils

import tw2.core
import tw2.rrd
import tw2.jqplugins.ui

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
    """ Main controller """

    # Mounting sub-controllers
    api = APIController()

    # Constants
    timespans = {
        'hour' : datetime.timedelta(hours=1),
        'day' : datetime.timedelta(days=1),
        'week' : datetime.timedelta(days=7),
        'month' : datetime.timedelta(days=31),
        'quarter' : datetime.timedelta(days=90),
        'year' : datetime.timedelta(days=365),
    }
    charts = {
        'history' : tw2.rrd.RRDJitAreaChart(
            id='some_id',
            offset=0,
            showAggregates=tw2.core.JSSymbol(src="""
                function(t, current, next, obj) {
                    return current.toFixed(1);
                }"""),
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
                    tip.innerHTML = "<b>" + elem.name + "</b>: " +
                                        elem.value.toFixed(1) +
                                        " hits per second.";
                })""")
            }
        ),
        'summary' : tw2.rrd.RRDProtoBarChart(
            id='some_id',
            p_height=700,
            p_width=900,
        ),
        'stream' : tw2.rrd.RRDStreamGraph(
            id='some_id',
            p_height=700,
            p_width=900,
        ),
    }
    # TODO -- get these categories from a tg config
    categories = ['filename', 'country']

    def __init__(self, *args, **kw):
        super(NarcissusController, self).__init__(*args, **kw)
        PolyButtonSet = tw2.jqplugins.ui.ButtonSetRadio(
            resources=tw2.jqplugins.ui.ButtonSetRadio.resources +
                [widgets.polyselect_css],
            click="""
function(e) {
    var chart = $('input[name=buttonset_charts]:checked').attr('id').substr(3);
    var category = $('input[name=buttonset_categories]:checked').attr('id').substr(3);
    var timespan = $('input[name=buttonset_timespans]:checked').attr('id').substr(3);
    window.location = '/chart/'+chart+'/'+category+'/'+timespan;
}""",
        )
        self.buttonset_widgets = [
            PolyButtonSet(
                id='buttonset_charts',
                items = [
                    {'id' : 'rb_' + key, 'label' : key.title() }
                    for key in self.charts.keys()
                ],
            ),
            PolyButtonSet(
                id='buttonset_categories',
                items = [
                    {'id' : 'rb_' + key, 'label' : key.title() }
                    for key in self.categories
                ],
            ),
            PolyButtonSet(
                id='buttonset_timespans',
                items = [
                    {'id' : 'rb_' + key, 'label' : key.title() }
                    for key, value in sorted(
                        list(self.timespans.iteritems()),
                        lambda x,y : cmp(x[1], y[1])
                    )
                ],
            ),
        ]

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

    @expose('mako:moksha.apps.narcissus.templates.about')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def about(self, *args, **kw):
        tmpl_context.readme = readme_as_html()
        return dict(option={})

    @expose('mako:moksha.apps.narcissus.templates.widgets')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def chart(self, *args, **kw):
        # Pad the arguments
        args = list(args) + ['__none__']*4
        chart, category, timespan = args[:3]
        default_url = '/chart/{chart}/{category}/{timespan}'

        if not chart in self.charts:
            chart = 'summary'
            redirect(default_url.format(**locals()))

        if not category in self.categories:
            category = 'country'
            redirect(default_url.format(**locals()))

        if not timespan in self.timespans:
            timespan = 'hour'
            redirect(default_url.format(**locals()))

        buttonsets = self.buttonset_widgets
        buttonsets[0] = buttonsets[0](checked_item='rb_' + chart)
        buttonsets[1] = buttonsets[1](checked_item='rb_' + category)
        buttonsets[2] = buttonsets[2](checked_item='rb_' + timespan)

        tmpl_context.widgets = buttonsets + [
            self.charts[chart](
                timedelta=self.timespans[timespan],
                rrd_filenames=get_rrd_filenames(category),
            ),
        ]
        return dict()
