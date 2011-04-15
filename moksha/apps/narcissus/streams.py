from datetime import timedelta, datetime
from moksha.api.hub.producer import PollingProducer

class NarcissusStream(PollingProducer):
    frequency = timedelta(seconds=5)
    topic = 'moksha.test'
    i = 0

    def poll(self):
        """ This method is called by the MokshaHub reactor every `frequency` """
        self.i += 1
        self.send_message(self.topic, {'message': self.i})
