import json

from collections import namedtuple

from file_forward.util import strict_update

from .base import LidoBase
from .lcb_header import LCBHeader
from .lcb_properties import LCBProperties

class LCBMessage(
    namedtuple('LCBMessage', field_names = ['header', 'properties']),
    LidoBase,
):
    """
    :param header: LCBHeader object.
    :param properties: LCBProperties object.
    """

    field_types = {
        'header': LCBHeader,
        'properties': LCBProperties,
    }

    # fields to nest into a key, when outputting nested style.
    nest_fields = {
        'header': 'JMSHeader',
        'properties': 'JMSProperties',
    }

    def get_header_fields(self):
        header_fields = {
            'JMSType': self.header.jms_type,
            'JMSExpiration': self.header.jms_expiration,
        }
        return header_fields

    def lido_meta_value(self):
        lido_meta = self.properties.lido_meta
        data = {
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
        return data

    def get_property_fields(self):
        property_fields = {
            'LidoMeta': json.dumps(self.lido_meta_value()),
        }
        return property_fields

    def get_fields(self):
        data = self.get_header_fields()
        strict_update(data, self.get_property_fields())
        return data
