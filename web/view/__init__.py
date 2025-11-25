from .index import index_bp
from .message_committed import message_committed_bp

def init_app(app):
    """
    Register blueprints on app.
    """
    app.register_blueprint(index_bp)
    app.register_blueprint(message_committed_bp, url_prefix='/log')
