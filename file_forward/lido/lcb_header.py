import xml.etree.ElementTree as ET

from collections import namedtuple

class LCBHeader(
    namedtuple(
        'LCBHeader',
        field_names = ['jms_expiration', 'jms_type'],
        defaults = [None, 'Byte'],
    ),
):
    """
    :param jms_type:
        Documents in payload will be sent in binary format (ZIP archive).
        Default fixed value: Byte
    :jms_expiration:
        Contains message’s expiration timestamp in milliseconds. Default
        expiration is set to 24h.
        Sample: 1546344000000
    """

    def as_dict(self):
        data = {
            'JMSType': self.jms_type,
        }
        if self.jms_expiration:
            data['JMSExpiration'] = self.jms_expiration
        return data

    def as_xml(self):
        """
        Return LCBHeader as XML element.
        """
        header = ET.Element('Header')
        ET.SubElement(header, 'JMSExpiration').text = self.jms_expiration
        ET.SubElement(header, 'JMSType').text = self.jms_type
        return header

    def iter_attrs(self):
        yield self.jms_expiration
        yield self.jms_type

    def iter_elements(self):
        for name, text in zip(self.__tags__, self.iter_attrs()):
            element = ET.Element(name)
            element.text = text
            yield element
