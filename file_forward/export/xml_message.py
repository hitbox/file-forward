import xml.etree.ElementTree as ET

from .base import MessageBase

class XMLMessage(MessageBase):
    """
    Build XML message from LCB data.
    """

    def __init__(self, style, root='root'):
        self.style = style
        self.root = root

    def get_header_nested(self, lcb_message):
        root = ET.Element()

    def get_header_string(self, lcb_message):
        """
        Return flat or nested header string, as configured.
        """
        header_fields = lcb_message.get_header_fields(lcb_message)
        property_fields = lcb_message.get_property_fields(lcb_message)

        header_elements = [element_with_text(key, str(val)) for key, val in header_fields.items()]
        property_elements = [element_with_text(key, str(val)) for key, val in property_fields.items()]

        root = ET.Element(self.root)

        if self.style == 'nested':

            header_element = ET.Element('JMSHeader')
            for key, val in header_fields.items():
                header_element.append(element_with_text(key, str(val)))

            property_element = ET.Element('JMSProperties')
            for key, val in property_fields.items():
                property_element.append(element_with_text(key, str(val)))

        elif self.style == 'flat':
            for fields in [header_fields, property_fields]:
                for key, val in fields.items():
                    root.append(element_with_text(key, str(val)))
        else:
            raise ValueError(f'Style not supported {self.style}')

        return ET.tostring(root, encoding='unicode')


def element_with_text(tagname, text, attrib={}, **extra):
    element = ET.Element(tagname, attrib=attrib, **extra)
    element.text = text
    return element
