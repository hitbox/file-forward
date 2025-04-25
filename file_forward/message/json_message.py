import json

from .base import MessageBase

class JSONMessage(MessageBase):
    """
    Build JSON message from LCB data.
    """

    def __init__(self, style):
        self.style = style

    def get_header_string(self, lcb_message):
        if self.style == 'nested':
            return json.dumps(lcb_message.as_dict())
        elif self.style == 'flat':
            return json.dumps(lcb_message.as_dict_flat())
        else:
            raise ValueError(f'Style not supported {self.style}')

    def log_entry(self, lcb_message, data=None):
        entry = self.get_header_string(lcb_message)
        if data is not None:
            entry += f'[DATA: {len(data)}]'
        return entry
