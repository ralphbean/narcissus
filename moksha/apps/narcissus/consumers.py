from moksha.api.hub import Consumer
from moksha.api.hub.producer import PollingProducer
from pprint import pformat
from pygeoip import GeoIP, GEOIP_MEMORY_CACHE
from datetime import timedelta
from subprocess import Popen, PIPE, STDOUT
from ansi2html import Ansi2HTMLConverter

import geojson
import simplejson
import threading

import logging
log = logging.getLogger(__name__)

_bucket_lock = threading.Lock()
_bucket = {}
def _dump_bucket():
    """ Returns and flushes the _bucket for the current timestep. """
    global _bucket_lock
    global _bucket
    with _bucket_lock:
        retval = _bucket
        _bucket = {}
    return retval

def _pump_bucket(key):
    """ Increments `key` in for the current timestep.  Thread safe. """
    global _bucket_lock
    global _bucket
    with _bucket_lock:
        _bucket[key] = _bucket.get(key, 0) + 1

AGGREGATE = 'aggregate'

class TimeSeriesProducer(PollingProducer):
    topic = 'http_metrics'
    n_timesteps = 15
    frequency = timedelta(seconds=3)
    history = {}
    jsonify = True

    def __init__(self, *args, **kw):
        super(TimeSeriesProducer, self).__init__(*args, **kw)
        self.history = { AGGREGATE : self._make_empty_hist() }

    def _make_empty_hist(self):
        return [0] * self.n_timesteps

    def add_timestamps(self, series):
        return [[i, series[i]] for i in range(self.n_timesteps)]

    def poll(self):
        bucket = _dump_bucket()

        # Convert units to "hits per second" so they're understandable
        for k in bucket.keys():
            bucket[k] = bucket[k] / float(self.frequency.seconds)

        # For any newly encountered keys, add a fake 'empty' history.
        for key in bucket:
            if key not in self.history:
                self.history[key] = self._make_empty_hist()

        # Add up a 'total' key for all keys in the current bucket.
        bucket[AGGREGATE] = sum(bucket.values())

        # Remove the oldest element in each history and add a 'zero'
        for key in self.history.keys():
            self.history[key] = self.history[key][1:] + [0]

        # Add the new bucket items to their histories
        for key in bucket.keys():
            self.history[key][-1] = bucket[key]

        # Convert from convenient 'self.history' internal repr to flot json
        json = {'data':[]}
        for key, series in self.history.iteritems():

            if key == AGGREGATE:
                continue

            json['data'].append({
                'data' : self.add_timestamps(series),
                'lines': {
                    'show': 'true',
                    'fill': 'true',
                },
                'label': key
            })

        self.send_message(self.topic, [json])



class TimeSeriesConsumer(Consumer):
    topic = 'httpdlight_http_rawlogs'
    jsonify = False

    def consume(self, message):
        if not message:
            return

        words = message.body.split()
        ip, location = words[0], words[6]

        if not '/' in location:
            return

        key = '(parsing error)'
        try:
            key = location.split('/')[1]
        except IndexError as e:
            pass

        _pump_bucket(key)

class HttpLightConsumer(Consumer):
    topic = 'httpdlight_http_rawlogs'
    jsonify = False

    geoip_url = '/'.join(__file__.split('/')[:-3] +
                         ["public/data/GeoLiteCity.dat"])
    gi = GeoIP(geoip_url, GEOIP_MEMORY_CACHE)

    def consume(self, message):
        if not message:
            #self.log.warn("%r got empty message." % self)
            return
        #self.log.debug("%r got message '%r'" % (self, message))
        words = message.body.split()
        rec = self.gi.record_by_addr(words[0])
        if words[0] and rec and rec['latitude'] and rec['longitude']:
            obj = {
                'ip' : words[0],
                'lat' : rec['latitude'],
                'lon' : rec['longitude'],
            }
            #self.log.debug("%r built %s" % (self, pformat(obj)))
            self.send_message('http_latlon', simplejson.dumps(obj))
        else:
            #self.log.warn("%r failed on '%s'" % (self, message))
            pass

class LatLon2GeoJsonConsumer(Consumer):
    topic = 'http_latlon'
    jsonify = True

    def consume(self, message):
        if not message:
            #self.log.warn("%r got empty message." % self)
            return
        #self.log.debug("%r got message '%s'" % (self, message))
        msg = message['body']

        feature = geojson.Feature(
            geometry=geojson.Point([msg['lon'], msg['lat']])
        )
        collection = geojson.FeatureCollection(features=[feature])
        obj = simplejson.loads(geojson.dumps(collection))
        self.send_message('http_geojson', obj)

class LogColorizer(Consumer):
    topic = 'httpdlight_http_rawlogs'
    jsonify = False

    converter = Ansi2HTMLConverter()

    def consume(self, message):
        if not message:
            return

        # This has got to be slow as all balls.  Can we do this in pure python?
        # TODO -- look into ripping code from pctail.  It is not nearly as good
        # as ccze, but it is in python so we can avoid dropping down through
        # subprocess.  It's also written like a nightmare but we can use it as a
        # starting point for our own colorizing.
        #       http://sourceforge.net/projects/pctail/
        p = Popen(['ccze', '-A'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
        ansi = p.communicate(input=message.body)[0]

        html = self.converter.convert(ansi, full=False).rstrip()

        obj = { 'html' : html }
        self.send_message('http_colorlogs', simplejson.dumps(obj))
