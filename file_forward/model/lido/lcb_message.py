import json
import logging

from collections import namedtuple

from file_forward.util import strict_update

from .base import LidoBase
from .lcb_header import LCBHeader
from .lcb_properties import LCBProperties

logger = logging.getLogger(__name__)

class LCBMessage(
    namedtuple('LCBMessage', field_names=['header', 'properties']),
    LidoBase,
):
    """
    Load Control Briefing Message.

    :param header: LCBHeader object.
    :param properties: LCBProperties object.
    """

    field_types = {
        'header': LCBHeader,
        'properties': LCBProperties,
    }

    @classmethod
    def from_source_result(cls, source_result, context=None):
        return cls(
            header = LCBHeader.from_source_result(source_result, context),
            properties = LCBProperties.from_source_result(source_result, context),
        )

    def get_header_fields(self):
        """
        Return dict of JMS Header properties.

        Relative path to docs:
        lcb/7.2.0-SR2449/api.html#jms-header
        """
        header_fields = {
            'JMSType': self.header.jms_type,
            'JMSExpiration': self.header.jms_expiration,
        }
        return header_fields

    def lido_meta_value(self):
        """
        Dict value for the LidoMeta to be turned into JSON.
        """
        lido_meta = self.properties.lido_meta
        value = {
            'legIdentifier': str(lido_meta.leg_identifier),
            'documents': [
                {
                    'docKey': document.doc_key,
                    'fileName': document.file_name,
                    'mediaType': document.media_type,
                }
                for document in lido_meta.documents
            ],
        }
        return value

    def get_property_fields(self):
        """
        Return dict of JMS Properties properties.

        Relative path to docs:
        lcb/7.2.0-SR2449/api.html#jms-properties
        """
        lido_meta = json.dumps(self.lido_meta_value())
        property_fields = {
            'LidoMeta': lido_meta,
        }
        return property_fields

    def get_fields(self):
        """
        Return header and properties as dict.
        """
        data = self.get_header_fields()
        strict_update(data, self.get_property_fields())
        return data
