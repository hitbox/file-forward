from flask import Blueprint
from flask import redirect
from flask import url_for

index_bp = Blueprint('index', __name__)

@index_bp.route('/')
def index():
    """
    Site index.
    """
    return redirect(url_for('message_committed.root'))
