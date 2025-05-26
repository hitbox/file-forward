from flask_sqlalchemy import SQLAlchemy

from file_forward.model import Base

db = SQLAlchemy(model_class=Base)

def init_app(app):
    """
    Initialize extensions against Flask application.
    """
    db.init_app(app)
