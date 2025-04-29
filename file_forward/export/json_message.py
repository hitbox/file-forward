import json

from file_forward.util import strict_update

from .base import MessageBase

class JSONMessage(MessageBase):
    """
    Build JSON message from LCB data.
    """

    def __init__(self, style):
        self.style = style

    def get_header_string(self, lcb_message):
        """
        Return flat or nested header string, as configured.
        """
        header_fields = lcb_message.get_header_fields(lcb_message)
        property_fields = lcb_message.get_property_fields(lcb_message)
        data = {}
        if self.style == 'nested':
            # Header and properties nested inside keys.
            data['JMSHeader'] = header_fields
            data['JMSProperties'] = property_fields
        elif self.style == 'flat':
            # All fields in one dict.
            strict_update(data, header_fields)
            strict_update(data, property_fields)
        else:
            raise ValueError(f'Style not supported {self.style}')

        return json.dumps(data)
