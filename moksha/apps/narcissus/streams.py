from datetime import timedelta, datetime
from moksha.api.hub.producer import PollingProducer

import simplejson
import geojson
import random

class NarcissusStream(PollingProducer):
    frequency = timedelta(seconds=1.5)
    topic = 'log2latlon'
    jsonify = True

    def produce_random_geojson(self):
        lat, lon = 37.775, -122.4183333  # SF Bay Area
        mod = lambda x : x + random.random() * 0.05 - 0.025

        json = geojson.FeatureCollection(
            features=[
                geojson.Feature(
                    geometry=geojson.Point([mod(lon), mod(lat)])
                )
            ]
        )

        # This is crazy, I know.  Geojson is weird and I'm not sure how it plays
        # with moksha's jsonify=True stuff above (it breaks).
        return simplejson.loads(geojson.dumps(json))


    def poll(self):
        """ This method is called by the MokshaHub reactor every `frequency` """

        json = self.produce_random_geojson()
        self.send_message(self.topic, json)

