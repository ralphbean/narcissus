#!/usr/bin/env python

from qpid.connection import Connection
from qpid.datatypes import Message, uuid4
from qpid.util import connect
import sys

import optparse
parser = optparse.OptionParser()
parser.add_option("-t", "--target", dest="target", default="localhost", help="target hostname running qpid")
parser.add_option("-d", "--debug", dest="debug", action="store_true", help="debug what messages are being sent")
options, args = parser.parse_args()

# Create connection and session
socket = connect(options.target, 5672)
connection = Connection(sock=socket, username='guest', password='guest')
connection.start()
session = connection.session(str(uuid4()))

# Setup queue
session.queue_declare(queue='message_queuefoobar')
session.exchange_bind(exchange='amq.topic', 
		queue='message_queuefoobar',
		binding_key='httpdlight_http_rawlogs')

# Setup routing properties
properties = session.delivery_properties(routing_key='httpdlight_http_rawlogs')


while True:
	msg = sys.stdin.readline()
	if not msg:
		break

	if options.debug:
		print "[sending]",msg

	session.message_transfer(
		destination='amq.topic',
		message=Message(properties, msg))
	

# Close session
session.close(timeout=10)
