from flask import Blueprint
from flask import redirect
from flask import render_template
from flask import url_for
from sqlalchemy import select

from web.extension import db

from file_forward.model import LegIdentifierModel
from file_forward.model import MessageCommitted
from file_forward.model import get_models
from htmlkit.orm import model_table

message_committed_bp = Blueprint('message_committed', __name__)

@message_committed_bp.route('/')
def root():
    """
    """
    stmt = db.select(MessageCommitted).order_by(MessageCommitted.logging_datetime)
    objects = db.session.scalars(stmt).all()
    context = {
        'objects': objects,
    }
    return render_template('message_committed.html', **context)
