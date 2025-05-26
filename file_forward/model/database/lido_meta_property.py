from markupsafe import escape
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import event
from sqlalchemy.orm import relationship

from .base import Base

class LidoMetaPropertyModel(Base):
    """
    Object describes flight leg to attach documents to.
    """

    __tablename__ = 'lido_meta_property'

    __ui_meta__ = {
        'leg_identifier' {
            'formatter': escape,
        },
    }

    id = Column(Integer, primary_key=True)

    leg_identifier_id = Column(
        Integer,
        ForeignKey('leg_identifier.id'),
        nullable = False,
    )

    leg_identifier = relationship('LegIdentifierModel')

    documents = relationship('DocumentModel')

    @classmethod
    def from_lido_meta_property(cls, lido_meta_property):
        return cls(**lido_meta_property._asdict())


@event.listens_for(LidoMetaPropertyModel.leg_identifier, 'set', retval=True)
def on_leg_identifier_set(target, value, oldvalue, initiator):
    """
    Change value to LegIdentifierModel.
    """
    from .leg_identifier import LegIdentifierModel
    from file_forward.model.lido import LegIdentifierField

    if isinstance(value, LegIdentifierField):
        # Convert namedtuple to database model
        value = LegIdentifierModel.from_leg_identifier_field(value)

    return value

@event.listens_for(LidoMetaPropertyModel.documents, 'append', retval=True)
def on_document_append(target, value, initiator):
    """
    Change value to DocumentModel.
    """
    from .document import DocumentModel
    from file_forward.model.lido import Document

    if isinstance(value, Document):
        # Convert namedtuple to database model
        value = DocumentModel.from_message_document(value)

    return value

@event.listens_for(LidoMetaPropertyModel.documents, 'bulk_replace', retval=True)
def on_document_append(target, document_list, initiator):
    """
    Change values to DocumentModel objects.
    """
    from .document import DocumentModel
    return [DocumentModel.from_message_document(document) for document in document_list]
