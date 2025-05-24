from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from file_forward.model import Base

class DocumentModel(Base):

    __tablename__ = 'document'

    id = Column(Integer, primary_key=True)

    doc_key = Column(String, nullable=False)
    file_name = Column(String, nullable=False)
    media_type = Column(String, nullable=False)

    lido_meta_property_id = Column(
        Integer,
        ForeignKey('lido_meta_property.id'),
    )

    @classmethod
    def from_message_document(cls, document):
        """
        Instantiate from document object used to create messages.
        """
        return cls(**document._asdict())
