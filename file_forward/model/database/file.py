import datetime
import enum

from sqlalchemy import CheckConstraint
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import Enum
from sqlalchemy import Float
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import validates

from file_forward.util import raise_for_empty_string

from .base import Base
from .mixin import UIMixin

class ProcessingState(enum.Enum):

    new = 'new'
    processed = 'processed'
    missing = 'missing'
    reappeared = 'reappeared'


class File(Base, UIMixin):

    __tablename__ = 'file'

    __ui_meta__ = {
        'path': {
            'label': 'Path',
            'td_attrs': {
                'class': 'data',
            },
        },
        'status': {
            'label': 'Status',
            'td_attrs': {
                'class': 'data',
            },
        },
    }

    id = Column(Integer, primary_key=True)

    path = Column(
        String,
        nullable = False,
        unique = True,
        doc = 'Original seen file path.',
    )

    seen_at = Column(
        DateTime,
        nullable = False,
        default = datetime.datetime.now,
        doc = 'Original seen at datetime of file.',
    )

    status = Column(
        Enum(ProcessingState),
        default = ProcessingState.new,
        doc = 'Last processing status of file.',
    )

    mtime = Column(
        Float,
        nullable = True,
        doc = 'Original mtime of file when first seen, as from stat() or similar.',
    )

    atime = Column(
        Float,
        nullable = True,
        doc = 'Original atime of file when first seen, as from stat() or similar.',
    )

    moved_to = Column(
        String,
        nullable = True,
        doc = 'The path the file was moved to after processing.',
    )

    @validates('path', 'moved_to')
    def validate_strings(self, key, value):
        return raise_for_empty_string(key, value)

    @classmethod
    def from_source_result(cls, file_obj):
        return cls(
            path = file_obj.path,
        )

    __table_args__ = (
        CheckConstraint("path <> ''"),
        CheckConstraint("moved_to <> ''"),
    )
