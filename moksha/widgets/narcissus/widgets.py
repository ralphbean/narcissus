from moksha.api.widgets.live import TW2LiveWidget
from tw2.polymaps import PolyMap

import logging
log = logging.getLogger(__name__)

class NarcissusWidget(TW2LiveWidget, PolyMap):
    topic = 'http_geojson'

    # TODO -- Yuck!  I shouldn't be using `eval()` here.  How should I do it?
    onmessage ="addGeoJsonToPolymap('${id}',eval(json), 10000)"

    zoom = 1

    # Let the user control the map
    interact = True

    # You should get your own one of these at http://cloudmade.com/register
    cloudmade_api_key = "1a1b06b230af4efdbb989ea99e9841af"

    # To style the map tiles
    cloudmade_tileset = 'pale-dawn'

    def prepare(self):
        # Weird thing about tw2 here --
        #       widgets don't know how to combine their
        #       parents resources on their own.  You have
        #       to do it manually.  :/
        # We could probably do this with the '__mro__' attr up in
        # tw2.core.Widget.
        self.resources = TW2LiveWidget.resources + PolyMap.resources
        super(NarcissusWidget, self).prepare()

