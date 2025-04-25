from . import logger
from .base import OutputBase

class LogOutput(OutputBase):
    """
    Write output to logs.
    """

    def __init__(self, build_message=None):
        self.build_message = build_message

    def __call__(self, source_result):
        lcb_message = source_result.as_lcb_message()

        if self.build_message:
            log_entry = self.build_message.log_entry(lcb_message, data=source_result.file_data)
        else:
            log_entry = source_result.ppstring()

        logger.debug(log_entry)
