from moksha.wsgi.widgets.api.live import LiveWidget
from tw2.polymaps import PolyMap
from tw2.jqplugins.jqplot.base import dateAxisRenderer_js
from tw2.slideymenu import MenuWidget

from moksha.wsgi.widgets.api.flot import LiveFlotWidget

import tw2.core as twc
import tw2.jquery

import logging
log = logging.getLogger(__name__)

modal_js = twc.JSLink(modname=__name__,
                      filename='static/js/modal.js')


def loading_dialog(href):
    return "javascript:loadingDialog('%s');" % href


class NarcissusMenu(MenuWidget):
    resources = MenuWidget.resources + [modal_js]
    id = 'awesome-menu'
    items = [
        {
            'label': 'Map (live)',
            'href': loading_dialog('/map'),
        }, {
            'label': 'Graph (live)',
            'href': loading_dialog('/graph'),
        # This is old code from the TG2/moksha-0.5 days.
        # ... left here for "historical purposes"
        #}, {
        #    'label': 'Monovariate',
        #    'href': loading_dialog('/chart/mono'),
        #}, {
        #    'label': 'Multivariate',
        #    'href': loading_dialog('/chart/multi'),
        #}, {
        #    'label': 'KML API',
        #    'href': loading_dialog('/api/google'),
        }, {
            'label': 'About',
            'href': loading_dialog('/about'),
        }
    ]

d3_js = twc.JSLink(
    modname=__name__,
    filename="static/js/d3/d3.min.js")
d3_geom_js = twc.JSLink(
    modname=__name__,
    filename="static/js/d3/d3.geom.min.js")
d3_layout_js = twc.JSLink(
    modname=__name__,
    filename="static/js/d3/d3.layout.min.js")

graphwidget_js = twc.JSLink(
    modname=__name__,
    filename="static/js/graph.js")
graphwidget_css = twc.CSSLink(
    modname=__name__,
    filename="static/css/graph.css")


class NarcissusGraphWidget(LiveWidget):
    template = "mako:narcissus.app.widgets.templates.graph"
    topic = 'graph_info'
    onmessage = """
    make_connection(json['country'], json['filename'].split('/')[1])
    """

    resources = LiveWidget.resources + [
        tw2.jquery.jquery_js,
        d3_js,
        d3_geom_js,
        d3_layout_js,
        graphwidget_js,
        graphwidget_css
    ]


green_css = twc.CSSLink(modname=__name__,
                        filename='static/css/custom_polymap.css')


class NarcissusMapWidget(LiveWidget, PolyMap):
    resources = LiveWidget.resources + PolyMap.resources + [green_css]
    topic = 'http_geojson'
    layer_lifetime = 1000

    onmessage = "addGeoJsonToPolymap('${id}', json, %i)" % layer_lifetime

    zoom = 2.1
    center_latlon = {'lat': 35.8, 'lon': -344.2}

    # Let the user control the map
    interact = True

    # Deep-linking
    hash = True

    # You should get your own one of these at http://cloudmade.com/register
    cloudmade_api_key = "1a1b06b230af4efdbb989ea99e9841af"

    # To style the map tiles
    cloudmade_tileset = 'midnight-commander'

    # Both specify the css_class AND include your own custom css file that
    # specifies what it looks like.
    css_class = 'midnight-commander-extras'


class NarcissusPlotWidget(LiveFlotWidget):
    name = 'Usage of http://mirror.rit.edu'
    topic = 'http_metrics'
    width = '100%'
    height = '100%'
    onmessage = """
        if (json == null) {
            return;
        } else {
            %s
        }
        """ % LiveFlotWidget.onmessage

logswidget_js = twc.JSLink(modname=__name__, filename="static/js/logs.js")
logswidget_css = twc.CSSLink(modname=__name__, filename="static/css/logs.css")


# TODO -- consider this for removal.  We onced used it to pipe logs through ccze
# and then through python-ansi2html and then over websockets to the browser.  it
# was hott, but insecure (piping to ccze in the shell allowed arbitrary remote
# code execution).  Can we do this "all in python"?
class NarcissusLogsWidget(LiveWidget):
    resources = LiveWidget.resources + [
        tw2.jquery.jquery_js,
        logswidget_js,
        logswidget_css,
    ]

    topic = 'http_colorlogs'
    onmessage = "addLogMessage('${id}', json)"
    template = "mako:moksha.widgets.narcissus.templates.logs"

polyselect_css = twc.CSSLink(modname=__name__,
                             filename='static/css/polyselect.css')


class PolyMonoButtonSet(tw2.jqplugins.ui.ButtonSetRadio):
    resources = tw2.jqplugins.ui.ButtonSetRadio.resources + [polyselect_css]

    click = """
        function(e) {
            var chart = $('input[name=buttonset_charts]:checked').attr('id').substr(3);
            var category = $('input[name=buttonset_categories]:checked').attr('id').substr(3);
            var timespan = $('input[name=buttonset_timespans]:checked').attr('id').substr(3);
            href = '/chart/mono/'+chart+'/'+category+'/'+timespan;
            loadingDialog(href);
        }"""


class PolyMultiButtonSet(tw2.jqplugins.ui.ButtonSetRadio):
    resources = tw2.jqplugins.ui.ButtonSetRadio.resources + [polyselect_css]

    click = """
        function(e) {
            var chart = $('input[name=buttonset_charts]:checked').attr('id').substr(3);
            var categories = $('input[name=buttonset_categories]:checked').attr('id').substr(5);
            var timespan = $('input[name=buttonset_timespans]:checked').attr('id').substr(3);
            console.log(categories);
            var cats = categories.split('___');
            var cat1 = cats[0];
            var cat2 = cats[1];

            href = '/chart/multi/'+chart+'/'+cat1+'/'+cat2+'/'+timespan;
            loadingDialog(href);
        }"""
