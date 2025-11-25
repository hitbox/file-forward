from markupsafe import escape
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base
from file_forward.model import lido as lidomod

class LCBMessageModel(Base):
    """
    Top-level LCB message object.
    """

    __tablename__ = 'lcb_message'

    __ui_meta__ = {
        'lcb_header': {
            'label': 'LCB Header',
            'formatter': escape,
        },
        'lcb_properties': {
            'label': 'LCB Properties',
            'formatter': escape,
        },
        'file': {
            'label': 'File',
            'formatter': escape,
        },
    }

    id = Column(Integer, primary_key=True)

    lcb_header_id = Column(
        Integer,
        ForeignKey('lcb_header.id'),
        nullable = False,
    )

    lcb_header = relationship(
        'LCBHeaderModel',
        back_populates = 'lcb_message',
    )

    lcb_properties_id = Column(
        Integer,
        ForeignKey('lcb_properties.id'),
        nullable = False,
    )

    lcb_properties = relationship(
        'LCBPropertiesModel',
        back_populates = 'lcb_message',
    )

    file_id = Column(ForeignKey('file.id'))

    file = relationship(
        'File',
        back_populates = 'lcb_messages',
    )

    @classmethod
    def from_source_result(cls, file_obj):
        from .lcb_header import LCBHeaderModel
        from .lcb_properties import LCBPropertiesModel

        lcb_message = lidomod.LCBMessage.from_source_result(file_obj)

        lcb_header = LCBHeaderModel(**lcb_message.header._asdict())
        lcb_properties = LCBPropertiesModel(**lcb_message.properties._asdict())

        instance = cls(lcb_header=lcb_header, lcb_properties=lcb_properties)
        return instance
