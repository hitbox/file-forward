import xml.etree.ElementTree as ET

from .base import MessageBase

class XMLMessage(MessageBase):
    """
    Build XML message from LCB data.
    """

    def __init__(self, style):
        self.style = style

    def get_header_string(self, lcb_message):
        if self.style == 'nested':
            return ET.tostring(lcb_message.as_xml(), encoding='unicode')
        elif self.style == 'flat':
            return ET.tostring(lcb_message.as_xml_flat(), encoding='unicode')
        else:
            raise ValueError(f'Style not supported {self.style}')

    def log_entry(self, lcb_message):
        return self.get_header_string(lcb_message)
