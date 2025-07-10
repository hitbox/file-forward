from markupsafe import Markup
from markupsafe import escape
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from .mixin import UIMixin

class DocumentModel(Base, UIMixin):

    __tablename__ = 'document'

    __ui_meta__ = {
        'doc_key': {
            'label': 'docKey',
            'td_attrs': {
                'class': 'data',
            },
        },
        'file_name': {
            'label': 'Filename',
            'td_attrs': {
                'class': 'data',
            },
        },
        'media_type': {
            'label': 'Media Type',
        },
        'lido_meta_property': {
            'label': 'Lido Meta Property',
            'formatter': lambda lido_meta_property:
                escape(lido_meta_property)
        },
    }

    id = Column(Integer, primary_key=True)

    doc_key = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    media_type = Column(String, nullable=False)

    lido_meta_property_id = Column(
        Integer,
        ForeignKey('lido_meta_property.id'),
    )

    lido_meta_property = relationship(
        'LidoMetaPropertyModel',
        back_populates = 'documents',
    )

    @classmethod
    def from_message_document(cls, document):
        """
        Instantiate from document object used to create messages.
        """
        return cls(**document._asdict())
