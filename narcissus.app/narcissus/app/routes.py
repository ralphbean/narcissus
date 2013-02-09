from flask import Flask, redirect
from flask.templating import render_template_string
from moksha.common.lib.helpers import get_moksha_appconfig
from moksha.wsgi.middleware import make_moksha_middleware
from moksha.wsgi.widgets.api import get_moksha_socket
from tw2.core.middleware import make_middleware

from narcissus.app.widgets import (
    NarcissusMenu,
    NarcissusMapWidget,
    NarcissusGraphWidget,
)

app = Flask(__name__)

simple_template = """
<html>
<head><title>Narcissus -- Realtime Log Visualization</title></head>
<body>
{{menu.display()}}
{{widget.display()}}
{{moksha_socket.display()}}
</body>
</html>
"""


@app.route("/")
def default():
    return redirect("/map")


@app.route("/<widget_name>/")
def basic(widget_name):

    # First, look up which widget we should render
    widgets = {
        'map': NarcissusMapWidget,
        'graph': NarcissusGraphWidget,
    }
    widget = widgets[widget_name]

    # Get config and mokshasocket resources
    config = get_moksha_appconfig()
    socket = get_moksha_socket(config)

    # Render that
    return render_template_string(
        simple_template,
        menu=NarcissusMenu(backend=config['moksha.livesocket.backend']),
        widget=widget(backend=config['moksha.livesocket.backend']),
        moksha_socket=socket,
    )


def main():
    # Load development.ini
    config = get_moksha_appconfig()

    # Wrap the inner wsgi app with our middlewares
    app.wsgi_app = make_moksha_middleware(app.wsgi_app, config)
    app.wsgi_app = make_middleware(app.wsgi_app)

    app.run(debug=True)

if __name__ == "__main__":
    main()
