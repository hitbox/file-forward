from flask import Blueprint
from flask import render_template
from sqlalchemy import select

from web.extension import db

from file_forward.model import LegIdentifierModel
from file_forward.model import get_models
from htmlkit.orm import model_table

core_bp = Blueprint('core', __name__)

@core_bp.context_processor
def context_processor():
    return {
        'title': 'File-Forward',
    }

@core_bp.route('/')
def index():
    """
    Site index.
    """
    context = {
        'subtitle': 'Index',
        'models': get_models(),
        'model_endpoint': 'core.list',
    }
    return render_template('base.html', **context)

@core_bp.route('/list/<model_name>')
def list(model_name):
    """
    List instances of model from name.
    """
    models = get_models()
    model = models[model_name]
    table = model_table(model)
    instances = db.session.scalars(select(model)).all()
    context = {
        'model': model,
        'instances': instances,
        'table': table,
    }
    return render_template('list_model.html', **context)

def init_app(app):
    """
    Register blueprints on app.
    """
    for obj in globals().values():
        if isinstance(obj, Blueprint):
            app.register_blueprint(obj)
