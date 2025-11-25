from markupsafe import escape
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import event
from sqlalchemy.orm import relationship

from .base import Base

class LCBPropertiesModel(Base):
    """
    """

    __tablename__ = 'lcb_properties'

    __ui_meta__ = {
        'lido_meta': {
            'label': 'Lido Meta',
            'formatter': escape,
        },
        'lido_application_id': {
        },
        'lido_business_id': {
        },
        'lido_client_id': {
        },
        'lido_customer_id': {
        },
        'lido_leg_identifier': {
        },
        'lido_msg_version': {
        },
        'lido_time_stamp': {
        },
        'lido_trace_id': {
        },
    }

    id = Column(Integer, primary_key=True)

    lcb_message = relationship(
        'LCBMessageModel',
        back_populates = 'lcb_properties',
    )

    lido_meta_id = Column(
        Integer,
        ForeignKey('lido_meta_property.id'),
        nullable = False,
    )

    lido_meta = relationship(
        'LidoMetaPropertyModel',
    )

    lido_application_id = Column(String, nullable=True)
    lido_business_id = Column(String, nullable=True)
    lido_client_id = Column(String, nullable=True)
    lido_customer_id = Column(String, nullable=True)
    lido_leg_identifier = Column(String, nullable=True)
    lido_msg_version = Column(String, nullable=True)
    lido_time_stamp = Column(String, nullable=True)
    lido_trace_id = Column(String, nullable=True)


@event.listens_for(LCBPropertiesModel.lido_meta, 'set', retval=True)
def on_lido_meta_set(target, value, oldvalue, initiator):
    """
    On LCBPropertiesModel.lido_meta set convert to model.
    """
    from file_forward.model.database import LidoMetaPropertyModel
    from file_forward.model.lido import LidoMetaProperty

    if isinstance(value, LidoMetaProperty):
        # Convert to model instance for database.
        value = LidoMetaPropertyModel.from_lido_meta_property(value)

    return value
