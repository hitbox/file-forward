from zoneinfo import ZoneInfo

from flask import Flask
from flask import current_app
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from . import extension
from . import view

def create_app():
    app = Flask(__name__)

    app.config.from_envvar('FILE_FORWARD_WEB_CONFIG')

    extension.init_app(app)
    view.init_app(app)

    @app.template_filter('localize')
    def localize(dt):
        """
        Jinja filter to localize to configured timezone.
        """
        timezone = current_app.config.get('FILE_FORWARD_TIMEZONE', 'UTC')
        timezone = ZoneInfo(timezone)

        fmt = current_app.config['FILE_FORWARD_DTFORMAT']
        localdt =  dt.astimezone(timezone)
        return localdt.strftime(fmt)

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
