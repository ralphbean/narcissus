#!/usr/bin/env python

# TODO -- there's a bug where the watched file gets moved out from under
# inotify.  We could address this with some pyinotify magic.
#
#   http://pyinotify.sourceforge.net/#The_EventsCodes_Class
#
# may need to watch IN_MOVE_* or something

import sys
import zmq

import optparse
parser = optparse.OptionParser()
parser.add_option("-t", "--targets", dest="targets",
                  default="tcp://127.0.0.1:11987",
                  help="comma-separated list of local publish endpoints")
parser.add_option("-p", "--topic", dest="topic",
                  default="httpdlight_http_rawlogs",
                  help="zeromq topic to talk on.")
parser.add_option("-d", "--debug", dest="debug", action="store_true",
                  help="debug what messages are being sent")


def main():
    options, args = parser.parse_args()

    options.targets = [t.strip() for t in options.targets.split(',')]

    ctx = zmq.Context()
    s = ctx.socket(zmq.PUB)

    # Create connection and session
    session_dicts = []
    for target in options.targets:
        print "Binding to %r for publishing" % target
        try:
            s.bind(target)
            print "    Created target", target
        except Exception as e:
            print "    Failed to create target", target
            print str(e)
            import traceback
            traceback.print_exc()

    print "Entering mainloop"
    while True:
        msg = sys.stdin.readline()
        if not msg:
            break

        if options.debug:
            print "[sending]", msg

        print options.topic, msg,
        s.send_multipart((options.topic, msg))

    s.close()
    ctx.destroy()
