from abc import ABC
from abc import abstractmethod

from file_forward.lido import LCBMessage

class MessageBase(ABC):

    separator = '\n---END-HEADER---\n'

    def __call__(self, source_result):
        """
        Convert source object into an encoded message.
        """
        header_string, separator, zipped_file_data = self.items(source_result)
        message = (header_string + self.separator).encode() + zipped_file_data
        return message

    def items(self, source_result):
        lcb_message = LCBMessage.from_source_result(source_result)
        zipped_file_data = source_result.zip_file_data()
        header_string = self.get_header_string(lcb_message)
        return (header_string, self.separator, zipped_file_data)

    @abstractmethod
    def get_header_string(self, lcb_message):
        """
        Get header that describes what Lido should do with data that will follow.
        """
