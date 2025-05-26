import csv

from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import UniqueConstraint
from sqlalchemy import select
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import validates

from file_forward.util import raise_for_empty_string

class CodePairMixin:
    """
    Mixin IATA and ICAO code pairs.
    """

    @declared_attr
    def code_iata(cls):
        return Column(
            String,
            nullable = False,
            info = {
                'label': 'IATA',
                'td_attrs': {
                    'class': 'data',
                },
            },
        )

    @declared_attr
    def code_icao(cls):
        return Column(
            String,
            nullable = False,
            info = {
                'label': 'ICAO',
                'td_attrs': {
                    'class': 'data',
                },
            },
        )

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

    @classmethod
    def load_many_from_csv(cls, path, iata_key, icao_key):
        """
        Load many instances from CSV.
        """
        with open(path, 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for data in csv_reader:
                kwargs = {
                    'code_iata': data[iata_key],
                    'code_icao': data[icao_key],
                }
                instance = cls(**kwargs)
                yield instance

    @classmethod
    def one_by_iata(cls, session, iata_code):
        """
        Get exactly one instance by IATA code, or raise.
        """
        stmt = select(cls).where(cls.code_iata == iata_code)
        return session.scalars(stmt).one()


class UIMixin:
    """
    Provide iterators for which attributes should be shown on user interfaces.
    """

    @declared_attr
    def __ui_meta__(cls):
        return {}

    @classmethod
    def get_ui_fields(cls):
        return list(cls.__ui_meta__)

    def get_ui_data(self):
        result = {}
        for field, opts in self.__ui_meta__.items():
            value = getattr(self, field)
            formatter = opts.get('formatter')
            if formatter:
                value = formatter(value)
            result[field] = value
        return result
