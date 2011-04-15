from moksha.api.hub import Consumer

class NarcissusConsumer(Consumer):

    # The message topic to listen to.
    topic = 'moksha.test'

    # Automatically decode message as JSON, and encode when using self.send_message
    jsonify = True

    def consume(self, message):
        self.log.info("%r.consume(%r)" % (self, message))
