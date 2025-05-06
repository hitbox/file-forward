from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import validates

from file_forward.util import raise_for_empty_string

from .base import Base

class SSLKeyRepository(Base):

    __tablename__ = 'sslkeyrepo'

    id = Column(Integer, primary_key=True)
    name = Column(
        String,
        unique = True,
        doc = 'Short descriptive name for SSL key repository.',
    )

    path = Column(String, nullable=False)

    certificate_label = Column(String, nullable=True)

    cipher_spec = Column(String, nullable=True)

    @validates('path', 'certificate_label', 'cipher_spec')
    def validate_strings(self, key, value):
        return raise_for_empty_string(key, value)

    __table_args__ = (
        CheckConstraint("path <> ''"),
        CheckConstraint("certificate_label <> ''"),
        CheckConstraint("cipher_spec <> ''"),
    )
