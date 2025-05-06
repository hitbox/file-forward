from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates

from file_forward.util import raise_for_empty_string

class CodePairMixin:

    @declared_attr
    def code_iata(cls):
        return Column(String, nullable=False)

    @declared_attr
    def code_icao(cls):
        return Column(String, nullable=False)

    @validates('code_iata', 'code_icao')
    def validate_strings(self, key, value):
        return raise_for_empty_string(key, value)

    @declared_attr
    def __table_args__(cls):
        return (
            UniqueConstraint('code_iata', 'code_icao'),
            CheckConstraint("code_iata <> ''"),
            CheckConstraint("code_icao <> ''"),
        )
