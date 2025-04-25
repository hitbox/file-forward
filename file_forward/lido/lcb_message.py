import json
import xml.etree.ElementTree as ET

from file_forward.util import strict_update

from .document import Document
from .lcb_header import LCBHeader
from .lcb_properties import LCBProperties
from .leg_identifier_field import LegIdentifierField
from .lido_meta_property import LidoMetaProperty

class LCBMessage:

    def __init__(self, header, properties):
        self.header = header
        self.properties = properties

    @classmethod
    def from_source_result(cls, source_result):
        """
        LCB message for Lido with metadata for PDF message. The zipped PDF goes
        in the message body.
        """
        return cls(
            LCBHeader(),
            LCBProperties.from_source_result(source_result),
        )

    def as_dict(self):
        """
        LCBMessage as data dict.
        """
        return {
            'header': self.header.as_dict(),
            'properties': self.properties.as_dict(),
        }

    def as_dict_flat(self):
        data = self.header.as_dict()
        strict_update(data, self.properties.as_dict())
        return data

    def as_json_string(self):
        """
        LCBMessage as JSON string.
        """
        return json.dumps(self.as_dict())

    def as_xml(self):
        root  = ET.Element('root')
        root.append(self.header.as_xml())
        root.append(self.properties.as_xml())
        return root

    def as_xml_flat(self):
        root  = ET.Element('root')

        for element in self.header.iter_elements():
            root.append(element)

        for element in self.properties.iter_elements():
            root.append(element)

        return root
