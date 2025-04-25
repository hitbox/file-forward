import xml.etree.ElementTree as ET

from .document import Document
from .lido_meta_property import LidoMetaProperty

class LCBProperties:

    __optional__ = [
        'lido_application_id',
        'lido_business_id',
        'lido_client_id',
        'lido_customer_id',
        'lido_leg_identifier',
        'lido_msg_version',
        'lido_time_stamp',
        'lido_trace_id',
    ]

    def __init__(
        self,
        *,
        lido_meta,
        lido_application_id = None,
        lido_business_id = None,
        lido_client_id = None,
        lido_customer_id = None,
        lido_leg_identifier = None,
        lido_msg_version = None,
        lido_time_stamp = None,
        lido_trace_id = None,
    ):
        """
        :param lido_meta:
            This mandatory property with crucial information for proper adding,
            replacing or removing documents to the correct briefing package.
            Detailed description below.
            JSON document.
        """
        self.lido_meta = lido_meta
        self.lido_application_id = lido_application_id
        self.lido_business_id = lido_business_id
        self.lido_client_id = lido_client_id
        self.lido_customer_id = lido_customer_id
        self.lido_leg_identifier = lido_leg_identifier
        self.lido_msg_version = lido_msg_version
        self.lido_time_stamp = lido_time_stamp
        self.lido_trace_id = lido_trace_id

    @classmethod
    def from_source_result(cls, source_result):
        instance = cls(
            lido_meta = LidoMetaProperty.from_source_result(source_result),
        )
        return instance

    def as_dict(self):
        data = {
            'LidoMeta': self.lido_meta.as_dict(),
        }
        for key in self.__optional__:
            value = getattr(self, key)
            if value:
                data[key] = value
        return data

    def as_xml(self):
        element = ET.Element('Properties')
        lido_meta = ET.SubElement(element, 'LidoMeta')
        lido_meta.append(self.lido_meta.as_xml())
        return element

    def iter_elements(self):
        # Element with JSON text.
        yield self.lido_meta.as_xml()
