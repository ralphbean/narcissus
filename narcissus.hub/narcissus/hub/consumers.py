""" consumers.py  -- where all the moksha-hub madness lives.

Diagram::

| narcissus/amqp-log-sender.py --------\
|                                      |
|                                      V
|                             <some qpid instance>
|                                      |
|                                      V
|                               The moksha-hub
|                                      |
|                                      V
|                        Topic:  httpdlight_http_rawlogs
|                                      |
|       /-----------------------------------\
|       |                                   |
|       V                                   V
|  LogColorizer             /------- HttpLightConsumer ---> sqlalchemy
|       |                   V               |
|       |           TimeSeriesConsumer      V
|       |                   |        LatLon2GeoJsonConsumer
|       |                   V               |
|       |               _bucket             |
|       |                   |               |
|       |                   V               |
|       V             TimeSeriesProducer    V
|    orbited                |            orbited
|       |                   V               |
|      *    *            orbited         ** |*
|   *   *  *    *          *|  *      *   *   * * *
|       *    *      *   * *  *   *      *   *       *
|       |         *  *THE INTERNET *        |
|       |              * *  *   *           |
|       V                *  |*              V
| NarcissusLogWidget        |       NarcissusMapWidget
|                           |
|                           |
|                           V
|                  NarcissusPlotWidget
"""

from moksha.hub.api import Consumer
from pygeoip import GeoIP
from pygeoip.const import GEOIP_MEMORY_CACHE
from datetime import datetime
from hashlib import md5

import geojson
import json
import re
import os

import logging
log = logging.getLogger(__name__)


def bobby_droptables(msg):
    """ Return true if `msg` might be Bobby's cousin. """

    dangerous_characters = [';', '<', '>', '&', '|']
    for danger in dangerous_characters:
        if danger in msg:
            return True

    return False


class RawIPConsumer(Consumer):
    """ Consumes dummy objects for testing like:
        {
            'ip': 'some_ip',
            'tag': 'some_tag',
        }
    """

    topic = 'narcissus.hits'
    jsonify = True

    # TODO -- get this location from config
    geoip_url = '/'.join([
        os.getcwd(), "data", "GeoLiteCity.dat",
    ])
    gi = GeoIP(geoip_url, GEOIP_MEMORY_CACHE)

    def consume(self, message):
        if not message:
            #self.log.warn("%r got empty message." % self)
            return
        #self.log.info("%r got message '%r'" % (self, message))
        message = json.loads(message['body'])

        # Get IP 2 LatLon info
        record = self.gi.record_by_addr(message['ip'])

        if not(record and record['latitude'] and record['longitude']):
            self.log.warn("Failed to geo-encode %r" % message)
            return

        updates = {
            'lat'           : record['latitude'],
            'lon'           : record['longitude'],
            'country'       : record.get('country_name', 'undefined'),
        }
        message.update(updates)

        self.send_message('http_latlon', message)

class HttpLightConsumer(Consumer):
    """ Main entry point of raw log messages.

    Responsible for:

        - Parsing raw logs
        - Logging to sqlalchemy
        - Sending parsed objects to other consumers

    """

    #app = 'narcissus' # this connects our ``self.DBSession``
    topic = 'httpdlight_http_rawlogs'
    jsonify = False

    # TODO -- get this location from config
    geoip_url = '/'.join([
        os.getcwd(), "data", "GeoLiteCity.dat",
    ])
    gi = GeoIP(geoip_url, GEOIP_MEMORY_CACHE)

    def __init__(self, *args, **kwargs):
        self.llre = re.compile('^(\d+\.\d+\.\d+\.\d+)\s(\S+)\s(\S+)\s\[(\S+\s\S+)\]\s"(\S+)\s(\S+)\s(\S+)"\s(\d+)\s(\d+)\s"(\S+)"\s"(.+)"\s(\d+)\s(\d+)$')
        super(HttpLightConsumer, self).__init__(*args, **kwargs)

    def consume(self, message):
        """ Main entry point for messages from the log-sender """
        if not message:
            #self.log.warn("%r got empty message." % self)
            return

        self.log.info("%r got message '%r'" % (self, message))

        regex_result = self.llre.match(message.body)

        if regex_result and regex_result.group(1):
            # Get IP 2 LatLon info
            record = self.gi.record_by_addr(regex_result.group(1))
            if record and record['latitude'] and record['longitude']:

                # Strip the timezone from the logged timestamp.  Python can't
                # parse it.
                no_timezone = regex_result.group(4).split(" ")[0]

                try:
                    # Format the log timestamp into a python datetime object
                    log_date = datetime.strptime(
                        no_timezone, "%d/%b/%Y:%H:%M:%S")
                except ImportError as e:
                    # There was some thread error.  Crap.
                    self.log.warn(str(e))
                    return

                # Build a big python dictionary that we're going to stream
                # around town (and use to build a model.ServerHit object.
                obj = {
                    'ip'            : regex_result.group(1),
                    'lat'           : record['latitude'],
                    'lon'           : record['longitude'],
                    'country'       : record.get('country_name', 'undefined'),
                    'logdatetime'   : log_date,
                    'requesttype'   : regex_result.group(5),
                    'filename'      : regex_result.group(6),
                    'tag'           : regex_result.group(6),
                    'httptype'      : regex_result.group(7),
                    'statuscode'    : regex_result.group(8),
                    'filesize'      : regex_result.group(9),
                    'refererhash'   : md5(regex_result.group(11)).hexdigest(),
                    'bytesin'       : regex_result.group(12),
                    'bytesout'      : regex_result.group(13),
                }

                # python datetime objects are not JSON serializable
                # We should make this more readable on the other side
                obj['logdatetime'] = str(obj['logdatetime'])

                #from pprint import pformat
                #self.log.debug("%r built %s" % (self, pformat(obj)))
                self.send_message('http_latlon', json.dumps(obj))
                self.send_message('graph_info', dict(
                    (key, obj[key]) for key in [
                        'country',
                        'tag',
                        'filename',
                    ]
                ))

            else:
                self.log.warn("%r geocode failed on '%s' with %r" % (
                    type(self).__name__,
                    message,
                    record,
                ))
        else:
            self.log.warn("regex failure.")

class LatLon2GeoJsonConsumer(Consumer):
    topic = 'http_latlon'
    jsonify = True

    def consume(self, message):
        if not message:
            #self.log.warn("%r got empty message." % self)
            return
        #self.log.debug("%r got message '%s'" % (self, message))
        msg = message['body']

        if isinstance(msg, basestring):
            msg = json.loads(msg)

        feature = geojson.Feature(
            geometry=geojson.Point([msg['lon'], msg['lat']])
        )
        collection = geojson.FeatureCollection(features=[feature])
        obj = json.loads(geojson.dumps(collection))
        self.send_message('http_geojson', obj)

## Raw colorized logs stuff ##

#class LogColorizer(Consumer):
#    topic = 'httpdlight_http_rawlogs'
#    jsonify = False
#
#    def __init__(self, *args, **kw):
#        from ansi2html import Ansi2HTMLConverter
#        self.converter = Ansi2HTMLConverter()
#        super(LogColorizer, self).__init__(*args, **kw)
#
#    def consume(self, message):
#        if not message:
#            return
#
#        # Look for dangerous injection stuff
#        if bobby_droptables(message.body):
#            self.log.warn("Bad message %s." % message)
#            return
#
#        # Pad the ip so the logs line up nice and straight.
#        # This is also slow.  Could we replace this with a regex?
#        ip, host, rest = message.body.split(' ', 2)
#        msg = "%16s %17s %s" % (ip, host, rest)
#
#        # This has got to be slow as all balls.  Can we do this in pure python?
#        # TODO -- look into ripping code from pctail.  It is not nearly as good
#        # as ccze, but it is in python so we can avoid dropping down through
#        # subprocess.  It's also written like a nightmare but we can use it as a
#        # starting point for our own colorizing.
#        #       http://sourceforge.net/projects/pctail/
#        p = Popen(['ccze', '-A'], stdout=PIPE, stdin=PIPE, stderr=STDOUT)
#        ansi = p.communicate(input=msg)[0]
#
#        html = self.converter.convert(ansi, full=False).rstrip()
#
#        obj = { 'html' : html }
#        self.send_message('http_colorlogs', json.dumps(obj))

## RRDTool stuff ##

#def _country_extractor(msg):
#    return msg['country']
#
#def _tag_extractor(msg):
#    tag = msg['tag']
#    if '/' not in tag:
#        return None
#
#    # Does this file really exist?
#    code = int(msg['statuscode'].strip())
#    if not (code >= 200 and code < 400):
#        return None
#
#    key = '(parsing error)'
#    try:
#        key = tag.split('/')[1]
#    except IndexError as e:
#        return None
#    return key
#
#key_extractors = {
#    'country' : _country_extractor,
#    'tag' : _tag_extractor,
#}
#
## A constant list of valid rrdtool categories.
## TODO -- this should be moved to the config
#rrd_categories = [
#    'country',
#    'tag',
#]
#
## Log pyrrd files to the current working directory.
## TODO -- pull this from configuration
#rrd_dir = os.getcwd() + '/rrds'
#
#import itertools
#import threading
#import time
#
#PAIRED = '__paired__'
#AGGREGATE = 'aggregate'
#_bucket_lock = threading.Lock()
#_bucket = {}
#def _dump_bucket():
#    """ Returns and flushes the _bucket for the current timestep. """
#    global _bucket_lock
#    global _bucket
#    with _bucket_lock:
#        retval = _bucket
#        _bucket = {}
#    return retval
#
#def _pump_bucket(category, key):
#    """ Increments `key` in for the current timestep.  Thread safe. """
#    global _bucket_lock
#    global _bucket
#    with _bucket_lock:
#        if not category in _bucket:
#            _bucket[category] = {}
#        _bucket[category][key] = _bucket[category].get(key, 0) + 1
#
#def _pump_paired_bucket(cat1, cat2, key1, key2):
#    """ Increments `key1` by `key2` in `cat1` by `cat2`. """
#    global _bucket_lock
#    global _bucket
#    with _bucket_lock:
#        if not PAIRED in _bucket:
#            _bucket[PAIRED] = {}
#
#        if not cat1 in _bucket[PAIRED]:
#            _bucket[PAIRED][cat1] = {}
#
#        if not cat2 in _bucket[PAIRED][cat1]:
#            _bucket[PAIRED][cat1][cat2] = {}
#
#        if not key1 in _bucket[PAIRED][cat1][cat2]:
#            _bucket[PAIRED][cat1][cat2][key1] = {}
#
#        _bucket[PAIRED][cat1][cat2][key1][key2] = \
#                _bucket[PAIRED][cat1][cat2][key1].get(key2, 0) + 1
#
#class TimeSeriesProducer(PollingProducer):
#    """ PollingProducer responsible for building time-series.
#
#    :class:`TimeSeriesConsumer` is an asynchronous consumer that stuffs messages
#    it receives into the module-global thread-safe `_bucket`.
#
#    This producer wakes up every `frequency` seconds, dumps the contents of
#    `_bucket` out and processes the contents.  It is responsible for:
#
#        - Keeping track of a time series in-memory for streaming graph
#        - Logging data to rrdtool for posterity
#
#    """
#
#    n_timesteps = 5
#    frequency = timedelta(seconds=3)
#    history = {}
#    jsonify = True
#
#    def __init__(self, *args, **kw):
#        super(TimeSeriesProducer, self).__init__(*args, **kw)
#        self.rrdtool_setup()
#        self.history = dict(
#            [(name, {AGGREGATE : self._make_empty_hist()})
#             for name in rrd_categories]
#        )
#
#    def _make_empty_hist(self):
#        return [0] * self.n_timesteps
#
#    def add_timestamps(self, series):
#        return [[i, series[i]] for i in range(self.n_timesteps)]
#
#    def poll(self):
#        __bucket = _dump_bucket()
#        for key in __bucket.keys():
#            if key is PAIRED:
#                self.process_paired_bucket(__bucket[key])
#            else:
#                self.process_bucket(
#                    series_name=key,
#                    bucket=__bucket[key]
#                )
#
#    def process_paired_bucket(self, paired):
#        for cat1 in paired.keys():
#            for cat2 in paired[cat1].keys():
#                for key1 in paired[cat1][cat2].keys():
#                    for key2 in paired[cat1][cat2][key1].keys():
#                        value = paired[cat1][cat2][key1][key2]
#                        self.rrdtool_log_paired(value, cat1, cat2, key1, key2)
#
#        # TODO -- As yet unimplemented!!!
#        # send off the appropriate amqp stuff for any listening live
#        # widgets (of which there are as yet none).
#
#    def process_bucket(self, series_name, bucket):
#        topic = 'http_counts_' + series_name
#
#        # Log to rrdtool
#        for k in bucket.keys():
#            self.rrdtool_log(bucket[k], series_name, k)
#
#        # Convert units to "hits per second" so they're understandable
#        for k in bucket.keys():
#            bucket[k] = bucket[k] / float(self.frequency.seconds)
#
#        # For any newly encountered keys, add a fake 'empty' history.
#        for key in bucket:
#            if key not in self.history[series_name]:
#                self.history[series_name][key] = self._make_empty_hist()
#
#        # Add up a 'total' key for all keys in the current bucket.
#        bucket[AGGREGATE] = sum(bucket.values())
#
#        # Remove the oldest element in each history and add a 'zero'
#        for key in self.history[series_name].keys():
#            self.history[series_name][key] = self.history[series_name][key][1:] + [0]
#
#        # Add the new bucket items to their histories
#        for key in bucket.keys():
#            self.history[series_name][key][-1] = bucket[key]
#
#        # Convert from convenient 'self.history' internal repr to flot json
#        json = {'data':[]}
#        for key, series in self.history[series_name].iteritems():
#
#            if key == AGGREGATE:
#                continue
#
#            json['data'].append({
#                'data' : self.add_timestamps(series),
#                'lines': {
#                    'show': True,
#                    'fill': False,
#                },
#                'label': key
#            })
#
#        self.send_message(topic, [json])
#
#    def rrdtool_setup(self):
#        """ Setup the rrdtool directory if this is the first run """
#
#        if not os.path.isdir(rrd_dir):
#            os.mkdir(rrd_dir)
#
#        for category in rrd_categories:
#            if not os.path.isdir(rrd_dir + '/' + category):
#                os.mkdir(rrd_dir + '/' + category)
#
#    def rrdtool_create(self, filename):
#        """ Create an rrdtool database if it doesn't exist """
#
#        # Create the directory if it doesn't exist.
#        directory = '/'.join(filename.split('/')[:-1])
#        if not os.path.isdir(directory):
#            os.makedirs(directory)
#
#        # Step interval for Primary Data Points (pdp)
#        pdp_step = self.frequency.seconds + (self.frequency.days * 86400)
#
#        # Heartbeat can be 'whatev', but twice the pdpd_step is good
#        heartbeat = 2 * pdp_step
#
#        # We only keep a single simple datasource.
#        sources = [
#            DataSource(
#                dsName='sum',
#                dsType='GAUGE',
#                heartbeat=heartbeat
#            )
#        ]
#
#        # TODO -- this should be a user-definable number.  It is equivalent to
#        # "how many data points do I want to see on any one graph at any given
#        # time."  The higher it is, the cooler your graphs look.  The higher it
#        # is, the more disk space is consumed.  The higher it is, the more
#        # memory is consumed client-side.
#        target_resolution = 60
#
#        # This function calculates how many PDP steps should be involved in the
#        # calculation of a single Consolidated Data Point (CDP).
#        cdp_steps = lambda tspan : (tspan / pdp_step) / target_resolution
#
#        # Just a lookup of how many seconds per 'timespan'
#        timespans = {
#            'hour'      : 3600,
#            'day'       : 86400,
#            'week'      : 604800,
#            'month'     : 2629744,
#            'quarter'   : 7889231,
#            'year'      : 31556926,
#        }
#
#        self.log.info("Building rrd %s.  %i cdp steps per hour." % (
#            filename, cdp_steps(timespans['hour'])))
#
#        # Here we build a series of round robin Archives of various resolutions
#        # and consolidation functions
#        archives = []
#        for consolidation_function in ['AVERAGE', 'MAX']:
#            archives += [
#                RRA(cf=consolidation_function, xff=0.5, rows=target_resolution,
#                    steps=cdp_steps(seconds_per_timespan))
#                for name, seconds_per_timespan in timespans.iteritems()
#            ]
#
#        # Actually build the round robin database from the parameters we built
#        rrd = RRD(
#            filename,
#            start=int(time.time()),
#            step=pdp_step,
#            ds=sources,
#            rra=archives,
#        )
#        rrd.create()
#
#    def safe_key(self, key):
#        """ rrdtool doesn't like spaces """
#        return key.replace(' ', '_')
#
#    def rrdtool_log_paired(self, count, cat1, cat2, key1, key2):
#        """ Log a message to a rrdtool db dedicated to comparing attributes """
#
#        key1 = self.safe_key(key1)
#        key2 = self.safe_key(key2)
#
#        if cat1 not in rrd_categories:
#            raise ValueError, "Invalid category 1 %s" % cat1
#
#        if cat2 not in rrd_categories:
#            raise ValueError, "Invalid category 2 %s" % cat2
#
#        filename = "/".join([rrd_dir, PAIRED, cat1, cat2, key1, key2 + '.rrd'])
#        self._rrdtool_log(count, filename)
#
#    def rrdtool_log(self, count, category, key):
#        """ Log a message to an category's corresponding rrdtool databse """
#
#        key = self.safe_key(key)
#
#        filename = rrd_dir + '/' + category + '/' + key + '.rrd'
#
#        if not category in rrd_categories:
#            raise ValueError, "Invalid category %s" % category
#
#        self._rrdtool_log(count, filename)
#
#    def _rrdtool_log(self, count, filename):
#        """ Workhorse for rrdtool logging.  Shouldn't be called directly. """
#
#        if not os.path.isfile(filename):
#            self.rrdtool_create(filename)
#            # rrdtool complains if you stuff data into a freshly created
#            # database less than one second after you created it.  We could do a
#            # number of things to mitigate this:
#            #   - sleep for 1 second here
#            #   - return from this function and not log anything only on the
#            #     first time we see a new data key (a new country, a new
#            #     filename).
#            #   - pre-create our databases at startup based on magical knowledge
#            #     of what keys we're going to see coming over the AMQP line
#            #
#            # For now, we're just going to return.
#            return
#
#        # TODO -- Is this an expensive operation (opening the RRD)?  Can we make
#        # this happen less often?
#        rrd = RRD(filename)
#
#        rrd.bufferValue(str(int(time.time())), str(count))
#
#        # This flushes the values to file.
#        # TODO -- Can we make this happen less often?
#        rrd.update()
#
#
#class TimeSeriesConsumer(Consumer):
#    topic = 'http_latlon'
#    jsonify = True
#
#    def consume(self, message):
#        """ Drop message metrics about country and filename into a bucket """
#        if not message:
#            return
#
#        for category in rrd_categories:
#            # key_extractors is a dict of callables
#            key = key_extractors[category](message['body'])
#            if key:
#                _pump_bucket(category, key)
#
#        for cat1, cat2 in itertools.product(rrd_categories, rrd_categories):
#            if cat1 == cat2:
#                # No point in pairing something with itself
#                continue
#
#            key1 = key_extractors[cat1](message['body'])
#            key2 = key_extractors[cat2](message['body'])
#            if key1 and key2:
#                _pump_paired_bucket(cat1, cat2, key1, key2)
