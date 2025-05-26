from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from . import extension
from . import view

def create_app():
    app = Flask(__name__)

    app.config.from_envvar('FILE_FORWARD_WEB_CONFIG')

    extension.init_app(app)
    view.init_app(app)

    # TODO
    # - Yet another web app
    # - Display my database info
    # - Probably need another load that associates files to messages
    # - Maybe missing other relevant info
    # - Need sent_at datetime for messages that can be none
    # - Add database step to LCBOutput class

    if 'APP_URL_PREFIX' in app.config:
        url_prefix = app.config['APP_URL_PREFIX'].rstrip('/')
        # Prefix all client side.
        app.config['SESSION_COOKIE_PATH'] = url_prefix
        # Prefix all routes.
        app.wsgi_app = DispatcherMiddleware(
            Flask('empty'),
            {
                url_prefix: app.wsgi_app,
            },
        )

    return app
