from moksha.api.widgets.live import LiveWidget
from moksha.widgets.moksha_js import moksha_js

class NarcissusWidget(LiveWidget):
    topic = 'moksha.test'
    params = ['id', 'topic']
    onmessage = """
        $('#chat_${id}').val(json.name + ': ' + json.message +
                             $('#chat_${id}').val())
    """
    javascript = [moksha_js]
    template = 'mako:moksha.widgets.narcissus.templates.widget'

    def update_params(self, d):
        super(NarcissusWidget, self).update_params(d)
