import ast

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import relationship

from .base import Base

class MessageCommitted(Base):
    """
    Data parsed from log lines.
    """
    # This is a stop gap until more full database objects can be created during
    # the main loop.

    __tablename__ = 'message_committed'

    id = Column(Integer, primary_key=True)

    logging_datetime = Column(
        DateTime(timezone=True),
        nullable = False,
    )

    logging_level_name = Column(String, nullable=False)

    logging_level_integer = Column(Integer, nullable=False)

    logger_name = Column(String, nullable=False)

    leg_identifiter_id = Column(
        Integer,
        ForeignKey('leg_identifier.id'),
        nullable = False,
    )

    leg_identifier = relationship(
        'LegIdentifierModel',
    )

    def logging_datetime_astimezone(self, timezone):
        return self.logging_datetime.astimezone(timezone)

    @classmethod
    def from_log_data(cls, session, data):
        """
        MessageCommitted instance from parsed log line data.
        """
        from .leg_identifier import LegIdentifierModel

        lido_meta_string = data['fields']['LidoMeta']
        lido_meta_data = ast.literal_eval(lido_meta_string)

        leg_identifier_string = lido_meta_data['legIdentifier']
        leg_identifier = LegIdentifierModel.from_leg_identifier_string(session, leg_identifier_string)

        message_committed = MessageCommitted(
            logging_datetime = data['logging_datetime'],
            logging_level_name = data['logging_level_name'],
            logging_level_integer = data['logging_level_integer'],
            logger_name = data['logger_name'],
            leg_identifier = leg_identifier,
        )
        return message_committed

    @classmethod
    def from_log_line(cls, session, line):
        """
        MessageCommitted instance from logging line text.
        """
        from file_forward.parse_log import parse_log_line

        try:
            data = parse_log_line(line)
        except ValueError:
            # Catch datetime conversion errors. If the first part of the log line
            # is not a datetime, ignore it.
            pass
        else:
            if data and set(['host', 'queue', 'fields']).issubset(data):
                return self.from_log_data(session, data)
