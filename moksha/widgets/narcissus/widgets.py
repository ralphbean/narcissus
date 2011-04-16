from moksha.api.widgets.live import TW2LiveWidget
from tw2.polymaps import PolyMap
import tw2.core as twc

import logging
log = logging.getLogger(__name__)

green_css = twc.CSSLink(modname=__name__,
                        filename='static/css/custom_polymap.css')

class NarcissusMapWidget(TW2LiveWidget, PolyMap):
    topic = 'http_geojson'
    layer_lifetime = 1000

    # TODO -- Yuck!  I shouldn't be using `eval()` here.  How should I do it?
    onmessage ="addGeoJsonToPolymap('${id}',eval(json), %i)" % layer_lifetime

    zoom = 1

    # Let the user control the map
    interact = True

    # You should get your own one of these at http://cloudmade.com/register
    cloudmade_api_key = "1a1b06b230af4efdbb989ea99e9841af"

    # To style the map tiles
    cloudmade_tileset = 'midnight-commander'

    # Both specify the css_class AND include your own custom css file that
    # specifies what it looks like.
    css_class = 'midnight-commander-extras'

    def prepare(self):
        # Weird thing about tw2 here --
        #       widgets don't know how to combine their
        #       parents resources on their own.  You have
        #       to do it manually.  :/
        # We could probably do this with the '__mro__' attr up in
        # tw2.core.Widget.
        self.resources = TW2LiveWidget.resources + PolyMap.resources
        self.resources.append(green_css)
        super(NarcissusMapWidget, self).prepare()

