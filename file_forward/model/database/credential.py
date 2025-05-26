from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import validates
from sqlalchemy_utils import PasswordType

from file_forward.util import raise_for_empty_string

from .base import Base

class Credential(Base):

    __tablename__ = 'credential'

    id = Column(Integer, primary_key=True)

    name = Column(
        String,
        unique = True,
        doc = 'Short descriptive name for credentials.',
    )
    username = Column(String, nullable=True)
    password = Column(PasswordType)

    @validates('username')
    def validate_strings(self, key, value):
        return raise_for_empty_string(key, value)
