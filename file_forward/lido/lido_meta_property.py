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
    :param leg_identifier: LegIdentifierField instance.
    :param documents: List of Document instances.
    """

    @classmethod
    def from_source_result(cls, source_result):
        """
        Return instance of LidoMetaProperty from source_result object.
        """
        instance = cls(
            leg_identifier = LegIdentifierField.from_source_result(
                source_result,
            ),
            documents = [
                Document.from_source_result(source_result),
            ],
        )
        return instance
