from datetime import timedelta, datetime
from moksha.api.hub.producer import PollingProducer

import random

class RandomIPProducer(PollingProducer):
    """ This is just for development. """
    frequency = timedelta(seconds=1.5)
    topic = 'httpdlight_http_rawlogs'

    def poll(self):
        """ This method is called by the MokshaHub reactor every `frequency` """

        self.log.info("poll was called")

        for i in range(random.randint(1, 10)):
            msg = '.'.join(map(str, (random.randint(0,127) for i in range(4))))
            self.log.info("%r sending %s" % (self, msg))
            self.send_message(self.topic, msg)
