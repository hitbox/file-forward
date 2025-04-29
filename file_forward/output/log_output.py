import logging

from .base import OutputBase

logger = logging.getLogger(__name__)

class LogOutput(OutputBase):
    """
    Write output to logs.
    """

    def __init__(self, message_builder=None, summarize_data=True):
        self.message_builder = message_builder
        self.summarize_data = summarize_data

    def __call__(self, source_result):
        lcb_message = source_result.as_lcb_message()

        source_string = source_result.log_entry()

        header, separator, zipped = self.message_builder.items(source_result)
        message_string = header + separator
        if self.summarize_data:
            message_string += f'[DATA: {len(source_result.file_data)}]'
        else:
            message_string = message_string.encode() + source_result.file_data

        logger.debug('%s:%s', source_string, message_string)
