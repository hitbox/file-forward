from abc import ABC
from abc import abstractmethod

from file_forward.lido import LCBMessage

from . import logger

class MessageBase(ABC):

    separator = '\n---END-HEADER---\n'

    def lcb_message_from_source_result(self, source_result):
        lcb_message = LCBMessage.from_source_result(source_result)
        return lcb_message

    def log_message(self, header, separator, data):
        logger.debug(f'%r[ZIP bytes: %s]', header + separator, len(data))

    def __call__(self, source_result):
        """
        Convert source object into an encoded message.
        """
        lcb_message = LCBMessage.from_source_result(source_result)
        data = source_result.zip_file_data()

        header_string = self.get_header_string(lcb_message)

        self.log_message(header_string, self.separator, data)
        message = (header_string + self.separator).encode() + data
        return message

    @abstractmethod
    def log_entry(self, lcb_message):
        """
        Return appropriate string for logging. Usually excludes or summarizes
        the file data.
        """

    @abstractmethod
    def get_header_string(self, lcb_message):
        """
        Get header that describes what Lido should do with data that will follow.
        """
