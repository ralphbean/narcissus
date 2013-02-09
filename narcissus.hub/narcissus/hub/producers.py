from datetime import timedelta, datetime
from moksha.hub.api.producer import PollingProducer

import simplejson
import random

class RandomIPProducer(PollingProducer):
    """ This is just for development. """
    frequency = timedelta(seconds=1.5)
    topic = 'narcissus.hits'

    def poll(self):
        """ This method is called by the MokshaHub reactor every `frequency` """

        for i in range(random.randint(1, 10)):
            ip = '.'.join(map(str, (random.randint(0,127) for i in range(4))))
            msg = simplejson.dumps({
                'ip': ip,
                'tag': "foo",
            })
            self.send_message(self.topic, msg)
