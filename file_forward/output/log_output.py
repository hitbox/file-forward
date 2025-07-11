import logging

from file_forward.model.lido import LCBMessage

from .base import OutputBase

logger = logging.getLogger(__name__)

class LogOutput(OutputBase):
    """
    Write output to logs.
    """

    def __init__(self, context=None):
        self.context = context

    def __call__(self, file):
        """
        Log file object as if it were written to some output.
        """
        lcb_message = LCBMessage.from_source_result(file, self.context)
        logger.debug('%s', lcb_message)

        message_fields = lcb_message.get_fields()
        logger.debug('%s', message_fields)

    def finalize(self):
        pass
