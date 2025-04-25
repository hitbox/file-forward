import json
import xml.etree.ElementTree as ET

from .document import Document
from .leg_identifier_field import LegIdentifierField

class LidoMetaProperty:
    """
    Example:
    {
      "legIdentifier": "2H.761.02Aug2019.FRA.MUC.L",
      "documents": [
        {
          "docKey": "TLR",
          "fileName": "TLR2.txt",
          "mediaType": "text/plain"
        },
        {
          "docKey": "APTMAP",
          "fileName": "FRA.pdf",
          "mediaType": "application/pdf"
        },
        {
          "docKey": "DOWI",
          "delete": true
        }
      ]
    }
    """

    def __init__(self, leg_identifier, documents):
        """
        :param leg_identifier:
            LegIdentifierField instance.
        :param documents:
            List of Document instances.
        """
        self.leg_identifier = leg_identifier
        self.documents = documents

    @classmethod
    def from_source_result(cls, source_result):
        instance = cls(
            leg_identifier = LegIdentifierField.from_opticlimb(
                source_result.path_data,
            ),
            documents = [
                Document.from_source_result(source_result),
            ],
        )
        return instance

    def as_dict(self):
        return {
            'legIdentifier': self.leg_identifier.as_string(),
            'documents': [document.as_dict() for document in self.documents],
        }

    def as_json_string(self):
        return json.dumps(self.as_dict())

    def as_xml(self):
        element = ET.Element('LidoMeta')
        element.text = self.as_json_string()
        return element
