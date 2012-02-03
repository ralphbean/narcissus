from tg import expose, validate, tmpl_context, redirect, session
from moksha.lib.base import Controller

from narcissus.decorators import (
    with_moksha_socket,
    with_ui_theme,
    with_menu
)
from narcissus.controllers.api import APIController
import narcissus.consumers
import narcissus.widgets as widgets
import moksha.utils

import tw2.core
import tw2.rrd
import tw2.jqplugins.ui

import docutils.examples
import datetime
import itertools
import os

import logging
log = logging.getLogger(__name__)

multi_categories = [(cat1, cat2) for cat1, cat2 in itertools.product(
    narcissus.consumers.rrd_categories,
    narcissus.consumers.rrd_categories,
) if cat1 != cat2]

def get_rrd_directories(cat1, cat2):
    basedir = '/'.join([narcissus.consumers.rrd_dir,
                        '__paired__', cat1, cat2])
    dirs = os.listdir(basedir)
    return [basedir + '/' + d + '/' for d in dirs]

def get_rrd_filenames(category):
    basedir = narcissus.consumers.rrd_dir + '/' + category + '/'
    files = os.listdir(basedir)
    return [basedir + f for f in files]

class ChartController(Controller):

    # TODO -- these should be shared between the consumers rrd-creation
    # timespans and here.

    # Constants
    timespans = {
        'hour' : datetime.timedelta(hours=1),
        'day' : datetime.timedelta(days=1),
        'week' : datetime.timedelta(days=7),
        'month' : datetime.timedelta(days=31),
        #'quarter' : datetime.timedelta(days=90),
        #'year' : datetime.timedelta(days=365),
    }

    multi_charts = {
        'bubble' : tw2.rrd.NestedRRDProtoCirclePackingWidget(
            id='some_id',
            p_height=700,
            p_width=900,
        ),
        'tree' : tw2.rrd.NestedRRDJitTreeMap(
            id='some_id',
            Tips = {
                'enable' : True,
                'offsetX' : 20,
                'offsetY' : 20,
                'onShow' : tw2.core.JSSymbol(src="""
                    (function(tip, node, isLeaf, domElement) {
                           var html = '<div class="tip-title">' + node.name
                             + '</div><div class="tip-text">';
                           var data = node.data;
                           if(data['$area']) {
                             html += ' hits per second:  ' + data['$area'].toFixed(2);
                           }
                           tip.innerHTML =  html;
                    })
                    """)
            },
            onCreateLabel = tw2.core.JSSymbol(src="""
                (function(domElement, node){
                   domElement.innerHTML = node.name;
                   var style = domElement.style;
                   style.display = '';
                   style.border = '1px solid transparent';
                   style.color = '#000000';
                   domElement.onmouseover = function() {
                     style.border = '1px solid #9FD4FF';
                   };
                   domElement.onmouseout = function() {
                     style.border = '1px solid transparent';
                   };
                } )
                """)
            ),
        }

    mono_charts = {
        'history' : tw2.rrd.FlatRRDJitAreaChart(
            id='some_id',
            offset=0,
            showAggregates=tw2.core.JSSymbol(src="""
                function(name, left, right, node, acum) {
                    return acum.toFixed(1);
                }"""),
            showLabels=False,
            # This won't work until Nico accepts my patch to thejit-proper
            #showLabels=tw2.core.JSSymbol(src="""
            #    function(name, left, right, node) {
            #        return 'hai';
            #    }"""),
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
        'summary' : tw2.rrd.FlatRRDProtoBarChart(
            id='some_id',
            p_height=700,
            p_width=900,
            hide_zeroes=True,
            # Sort by total value
            series_sorter = lambda self, x, y: -1 * cmp(
                sum([d[1] for d in x['data']]),
                sum([d[1] for d in y['data']])
            )
        ),
        'bubble' : tw2.rrd.FlatRRDProtoBubbleChart(
            id='some_id',
            p_height=700,
            p_width=900,
        ),
        'stream' : tw2.rrd.FlatRRDStreamGraph(
            id='some_id',
            p_height=700,
            p_width=900,
        ),
    }

    def __init__(self, *args, **kw):
        super(ChartController, self).__init__(*args, **kw)
        self.sorted_timespan_names = [key for key, value in sorted(
            list(self.timespans.iteritems()),
            lambda x,y : cmp(x[1], y[1])
        )]

        self.mono_buttonset_widgets = [
            widgets.PolyMonoButtonSet(
                id='buttonset_charts',
                items = [
                    {'id' : 'rb_' + key, 'label' : key.title() }
                    for key in self.mono_charts.keys()
                ],
            ),
            widgets.PolyMonoButtonSet(
                id='buttonset_categories',
                items = [
                    {'id' : 'rb_' + key, 'label' : key.title() }
                    for key in narcissus.consumers.rrd_categories
                ],
            ),
            widgets.PolyMonoButtonSet(
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
        self.multi_buttonset_widgets = [
            widgets.PolyMultiButtonSet(
                id='buttonset_charts',
                items = [
                    {'id' : 'rb_' + key, 'label' : key.title() }
                    for key in self.multi_charts.keys()
                ],
            ),
            widgets.PolyMultiButtonSet(
                id='buttonset_categories',
                items = [
                    {'id' : '___'.join(['rb', key1, key2]),
                     'label' : (key1 + ' vs. ' + key2).title() }
                    for key1, key2 in multi_categories
                ],
            ),
            widgets.PolyMultiButtonSet(
                id='buttonset_timespans',
                items = [
                    {'id' : 'rb_' + key, 'label' : key.title() }
                    for key in self.sorted_timespan_names
                ],
            ),
        ]

    @expose()
    def index(self, *args, **kw):
        redirect('/mono')

    @expose('mako:narcissus.templates.widgets')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def mono(self, *args, **kw):
        # Pad the arguments
        args = list(args) + ['__none__']*4
        chart, category, timespan = args[:3]
        default_url = '/chart/mono/{chart}/{category}/{timespan}'

        if not chart in self.mono_charts:
            chart = self.mono_charts.keys()[0]
            redirect(default_url.format(**locals()))

        if not category in narcissus.consumers.rrd_categories:
            category = narcissus.consumers.rrd_categories[0]
            redirect(default_url.format(**locals()))

        if not timespan in self.timespans:
            timespan = self.sorted_timespan_names[0]
            redirect(default_url.format(**locals()))

        buttonsets = self.mono_buttonset_widgets
        buttonsets[0] = buttonsets[0](checked_item='rb_' + chart)
        buttonsets[1] = buttonsets[1](checked_item='rb_' + category)
        buttonsets[2] = buttonsets[2](checked_item='rb_' + timespan)

        tmpl_context.widgets = buttonsets + [
            self.mono_charts[chart](
                timedelta=self.timespans[timespan],
                rrd_filenames=get_rrd_filenames(category),
            ),
        ]
        return dict()

    @expose('mako:narcissus.templates.widgets')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def multi(self, *args, **kw):
        # Pad the arguments
        args = list(args) + ['__none__']*5
        chart, cat1, cat2, timespan = args[:4]
        default_url = '/chart/multi/{chart}/{cat1}/{cat2}/{timespan}'

        if not chart in self.multi_charts:
            chart = self.multi_charts.keys()[0]
            redirect(default_url.format(**locals()))

        if not cat1 in narcissus.consumers.rrd_categories:
            cat1 = narcissus.consumers.rrd_categories[0]
            redirect(default_url.format(**locals()))

        if not cat2 in narcissus.consumers.rrd_categories:
            cat2 = narcissus.consumers.rrd_categories[1]
            redirect(default_url.format(**locals()))

        if not timespan in self.timespans:
            timespan = self.sorted_timespan_names[0]
            redirect(default_url.format(**locals()))

        buttonsets = self.multi_buttonset_widgets
        buttonsets[0] = buttonsets[0](checked_item='rb_' + chart)
        buttonsets[1] = buttonsets[1](
            checked_item='___'.join(['rb', cat1, cat2]))
        buttonsets[2] = buttonsets[2](checked_item='rb_' + timespan)

        tmpl_context.widgets = buttonsets + [
            self.multi_charts[chart](
                root_title = (cat1 + ' vs. ' + cat2).title(),
                timedelta=self.timespans[timespan],
                rrd_directories=get_rrd_directories(cat1, cat2),
            ),
        ]
        return dict()

