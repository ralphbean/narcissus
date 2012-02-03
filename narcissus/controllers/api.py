from tg import expose, session, request
from moksha.lib.base import Controller
from sqlalchemy.sql.expression import between

import narcissus.model as m
import kmlcircle
import datetime

import logging
log = logging.getLogger(__name__)

def iplatloncreate():
    serverhits=m.ServerHit.query.filter(m.ServerHit.insdatetime>=(datetime.datetime.now()-datetime.timedelta(seconds=1))).limit(4000).all()
    # If only google actually supported sessions! Darn them!
    #if 'datetime' in session:
    #    session['oldolddatetime'] = session.get('olddatetime')
    #    session['olddatetime'] = session.get('datetime')
    #else:
    #    session['olddatetime'] = tmpdate
    #session['datetime'] = serverhits[-1].insdatetime
    for row in serverhits:
        yield {
            'name': 'IP: %s' % row.ip,
            'description': 'Bytes: %s' % row.bytesout,
            'circle': kmlcircle.kml_regular_polygon(row.lon,row.lat,
                                                    kmlcircle.log(row.bytesout)*1000),
            'id': row.id
            }

    #session.save()

def iplatlondel():
# If only google actually supported sessions! Darn them!
#    if 'oldolddatetime' in session:
#        serverhits=m.ServerHit.query.filter(between(m.ServerHit.insdatetime,session.get('oldolddatetime'),session.get('olddatetime'))).limit(4000).all()
    serverhits=m.ServerHit.query.filter(between(m.ServerHit.insdatetime,datetime.datetime.now()-datetime.timedelta(seconds=8),datetime.datetime.now()-datetime.timedelta(seconds=2))).all()
    for row in serverhits:
        yield {
            'del': '<Placemark targetId="A'+str(row.id)+'"></Placemark>'
        }

class APIController(Controller):

    @expose('genshi:narcissus.templates.kml')
    def kml(self, *args, **kw):
        return dict(
            create=iplatloncreate(),delete=iplatlondel(),
            baseurl=request.application_url + '/api',
        )

    @expose('genshi:narcissus.templates.kmlinit')
    def kmlinit(self, *args, **kw):
        return dict(
            baseurl=request.application_url + '/api',
        )

    @expose('genshi:narcissus.templates.google')
    def google(self, *args, **kw):
        import pprint
        log.warn(pprint.pformat(request))
        log.warn(pprint.pformat(request.__dict__))
        return dict(
            baseurl=request.application_url + '/api',
        )
