from tg import expose, validate, tmpl_context, redirect, session
from moksha.lib.base import Controller

from sqlalchemy.sql.expression import between

from datetime import datetime, timedelta

from moksha.apps.narcissus.decorators import (
    with_moksha_socket,
    with_ui_theme,
    with_menu
)

import docutils.examples

import moksha.utils
import kmlcircle
import logging
log = logging.getLogger(__name__)
import moksha.apps.narcissus.model as m

def readme_as_html():
    """ Ridiculous """
    root = '/'.join(__file__.split('/')[:-4])
    fname = root + '/README.rst'
    with open(fname, 'r') as f:
        readme = f.read()
        readme = readme.split('.. split here')[1]
        return docutils.examples.html_body(unicode(readme))

def iplatloncreate():
    tmpdate=datetime.now()-timedelta(seconds=1)
    serverhits=m.ServerHit.query.filter(m.ServerHit.insdatetime>=session.get('datetime',tmpdate)).limit(3000).all()
    if 'datetime' in session:
        session['oldolddatetime'] = session.get('olddatetime')
        session['olddatetime'] = session.get('datetime')
    else:
        session['olddatetime'] = tmpdate
    session['datetime'] = serverhits[-1].insdatetime
    for row in serverhits:
        yield {
            'name': 'IP: %s' % row.ip,
            'description': 'Bytes: %s' % row.bytesout,
            'circle': kmlcircle.kml_regular_polygon(row.lon,row.lat,
                                                    kmlcircle.log(row.bytesout)*1000),
            'id': row.id
            }

    session.save()

def iplatlondel():
    if 'oldolddatetime' in session:
        serverhits=m.ServerHit.query.filter(between(m.ServerHit.insdatetime,session.get('oldolddatetime'),session.get('olddatetime'))).limit(4000).all()
        for row in serverhits:
            yield {
                'del': '<Placemark targetId="A'+str(row.id)+'"></Placemark>'
            }

class NarcissusController(Controller):

    @expose()
    def index(self, *args, **kw):
        redirect('/map')

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def countries(self, *args, **kw):
        tmpl_context.widget = moksha.utils.get_widget('narc_plot')(
            topic='http_counts_country')
        return dict(options={})

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def filenames(self, *args, **kw):
        tmpl_context.widget = moksha.utils.get_widget('narc_plot')(
            topic='http_counts_filename')
        return dict(options={})

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def map(self, *args, **kw):
        tmpl_context.widget = moksha.utils.get_widget('narc_map')
        return dict(options={})

    @expose('mako:moksha.apps.narcissus.templates.widget')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def logs(self, *args, **kw):
        tmpl_context.widget = moksha.utils.get_widget('narc_logs')
        return dict(options={})

    @expose('mako:moksha.apps.narcissus.templates.about')
    @with_moksha_socket
    @with_menu
    @with_ui_theme
    def about(self, *args, **kw):
        tmpl_context.readme = readme_as_html()
        return dict(option={})

    @expose('genshi:moksha.apps.narcissus.templates.kml')
    def kml(self, *args, **kw):
        return dict(create=iplatloncreate(),delete=iplatlondel())

    @expose('genshi:moksha.apps.narcissus.templates.kmlinit')
    def kmlinit(self, *args, **kw):
        return dict()

    @expose('genshi:moksha.apps.narcissus.templates.google')
    def google(self, *args, **kw):
        return dict()
