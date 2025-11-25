import string

from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Time
from sqlalchemy import select
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy

from file_forward.model.lido.leg_identifier_field import DATE_OF_ORIGIN_FORMAT
from file_forward.util import raise_for_empty_string

from .base import Base
from .mixin import UIMixin

class AircraftRegistration(Base):

    __tablename__ = 'aircraft_registration'

    id = Column(Integer, primary_key=True)

    aircraft_registration = Column(String, nullable=False)

    @validates('aircraft_registration')
    def validate(self, key, value):
        raise_for_empty_string(key, value)
        return value

    @classmethod
    def get_or_create(cls, session, aircraft_registration):
        stmt = select(cls).where(cls.aircraft_registration == aircraft_registration)
        instance = session.scalars(stmt).one_or_none()
        if instance is None:
            instance = cls(aircraft_registration=aircraft_registration)
            session.add(instance)
        return instance
