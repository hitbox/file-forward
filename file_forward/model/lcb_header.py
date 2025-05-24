from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from file_forward.model import Base

class LCBHeaderModel(Base):
    """
    Header part of LCB message.
    """

    __tablename__ = 'lcb_header'

    id = Column(Integer, primary_key=True)

    jms_type = Column(String, nullable=False)

    jms_expiration = Column(
        Integer,
        nullable = True,
        doc =
            'Contains message’s expiration timestamp in milliseconds.'
            ' Default expiration is set to 24h. Sample: 1546344000000',
    )
