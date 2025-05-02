from collections import namedtuple

from .document import Document
from .leg_identifier_field import LegIdentifierField
from .base import LidoBase

class LidoMetaProperty(
    namedtuple(
        'LidoMetaProperty',
        field_names = ['leg_identifier', 'documents'],
    ),
    LidoBase,
):
    """
    Represents a message property that maps to a specific flight leg and its
    associated documents.

    This object is used in LCB messages to specify which flight leg's documents
    should be updated or overwritten. It wraps a `leg_identifier` (which
    identifies the leg) and a list of `documents` associated with that leg.

    :param leg_identifier: LegIdentifierField instance.
    :param documents: List of Document instances.
    """

    @classmethod
    def from_source_result(cls, source_result, context):
        """
        Return instance of LidoMetaProperty from source_result object.
        """
        instance = cls(
            leg_identifier = LegIdentifierField.from_source_result(
                source_result,
                context,
            ),
            documents = [Document.from_source_result(source_result, context=context)],
        )
        return instance
