#!/usr/bin/env python

from qpid.connection import Connection
from qpid.datatypes import Message, uuid4
from qpid.util import connect
import sys

import optparse
parser = optparse.OptionParser()
parser.add_option("-t", "--targets", dest="targets", default="localhost",
                  help="comma-separated list of target hostnames running qpid")
parser.add_option("-p", "--topic", dest="topic",
                  default="httpdlight_http_rawlogs",
                  help="amqp topic to talk on.")
parser.add_option("-d", "--debug", dest="debug", action="store_true",
                  help="debug what messages are being sent")
options, args = parser.parse_args()

options.targets = [t.strip() for t in options.targets.split(',')]

# Create connection and session
session_dicts = []
for target in options.targets:
    print "Attempting to setup connection with", target
    try:
        socket = connect(target, 5672)
        connection = Connection(
            socket, username='guest', password='guest',
        )
        connection.start(timeout=10000)
        session = connection.session(str(uuid4()))

        # Setup routing properties
        print "Talking to %s on topic %s" % (target, options.topic)
        properties = session.delivery_properties(routing_key=options.topic)
        session_dicts.append({
            'target' : target,
            'socket' : socket,
            'connection' : connection,
            'session' : session,
            'properties' : properties,
        })
        print "    Created target", target
    except Exception as e:
        print "    Failed to create target", target
        print str(e)
        import traceback
        traceback.print_exc()


print "Entering mainloop"
print "Sending to", ",".join([d['target'] for d in session_dicts])
while True:
    msg = sys.stdin.readline()
    if not msg:
        break

    if options.debug:
        print "[sending]",msg

    for d in session_dicts:
        d['session'].message_transfer(
            destination='amq.topic',
            message=Message(d['properties'], msg))


# Close session
for d in session_dicts:
    d['session'].close(timeout=10)
