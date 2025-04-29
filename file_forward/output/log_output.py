import logging

from file_forward.lido import LCBMessage

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
        """
        Log source_result object as if it were written to some output.
        """
        lcb_message = LCBMessage.from_source_result(source_result)

        source_string = source_result.log_entry()

        header, separator, zipped = self.message_builder.items(source_result)
        message_string = header + separator
        if self.summarize_data:
            message_string += f'[DATA: {len(source_result.file_data)}]'
        else:
            message_string = message_string.encode() + source_result.file_data

        logger.debug('%s:%s', source_string, message_string)
