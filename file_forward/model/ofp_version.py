from collections import namedtuple

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String

from .base import Base

class OFPVersion(
    namedtuple(
        'OFPVersion',
        field_names = [
            'ofp_version_major',
            'ofp_version_minor',
            'ofp_version_patch',
        ],
        defaults = [
            0,
            0,
            0,
        ],
    ),
):
    """
    Named tuple of the three parts of an OFP version--the major, minor, and patch integers.
    """


class __OFPVersion(Base):

    __tablename__ = 'ofp_version'

    id = Column(Integer, primary_key=True)

    major = Column(Integer, nullable=False, default=0)
    minor = Column(Integer, nullable=False, default=0)
    patch = Column(Integer, nullable=False, default=0)

    def as_string(self):
        return '.'.join([self.major, self.minor, self.patch])
