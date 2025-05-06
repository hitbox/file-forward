import logging

from file_forward.model.lido import LCBMessage

from .base import OutputBase

logger = logging.getLogger(__name__)

class LogOutput(OutputBase):
    """
    Write output to logs.
    """

    def __init__(self, message_builder=None, summarize_data=True, context=None):
        self.message_builder = message_builder
        self.summarize_data = summarize_data
        self.context = context

    def __call__(self, file):
        """
        Log file object as if it were written to some output.
        """
        lcb_message = LCBMessage.from_source_result(file, self.context)

        header, separator, zipped = self.message_builder.items(file)
        message_string = header + separator
        if self.summarize_data:
            message_string += f'[DATA: {len(file.file_data)}]'
        else:
            message_string = message_string.encode() + file.file_data

        logger.debug('%s:%s:%s', file.client.name, file.path, message_string)

    def finalize(self):
        pass
