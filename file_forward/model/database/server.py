from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import validates

from file_forward.util import raise_for_empty_string

from .base import Base

class Server(Base):

    __tablename__ = 'server'

    id = Column(Integer, primary_key=True)

    host = Column(String, unique=True, doc='Host name.')

    port = Column(Integer, doc='Port number.')

    name = Column(
        String,
        unique = True,
        nullable = False,
        doc = 'Short descriptive name for host.',
    )

    description = Column(
        Text,
        nullable = True,
        doc = 'Server description.',
    )

    @validates('name', 'description')
    def validate_string(self, key, value):
        return raise_for_empty_string(key, value)
