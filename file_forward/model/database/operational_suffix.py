from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import validates

from .base import Base

class OperationalSuffix(Base):

    __tablename__ = 'operational_suffix'

    id = Column(Integer, primary_key=True)

    letter = Column(String, nullable=False, unique=True)

    description = Column(Text, nullable=True)

    @validates('letter', 'description')
    def validate_strings(self, key, value):
        return raise_for_empty_string(key, value)

    __table_args__ = (
        CheckConstraint("letter <> ''"),
        CheckConstraint("description <> ''"),
    )
