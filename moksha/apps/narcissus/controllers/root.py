from tg import expose, validate
from formencode import validators
from moksha.lib.base import Controller

class NarcissusController(Controller):

    @expose('mako:moksha.apps.narcissus.templates.index')
    @validate({'name': validators.UnicodeString()})
    def index(self, name='world', *args, **kw):
        return dict(name=name)
