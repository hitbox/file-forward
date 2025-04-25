from file_forward.util import decode_md

from . import logger
from .base import OutputBase

class LCBOutput(OutputBase):
    """
    Write Lido LCB message to client.
    """

    def __init__(self, client, build_message):
        """
        :param client:
            Message queue client.
        :param build_message:
            Callable to build message for queue.
        """
        self.client = client
        self.build_message = build_message

    def __call__(self, source_result):
        message = self.build_message(source_result)
        with self.client as message_queue:
            message_descriptor = message_queue.put(message)
            message_queue.commit()

            # Log resulting message descriptor.
            md_data = decode_md(message_descriptor)
            logger.info(
                'message committed.'
                f' MsgId={md_data.get("MsgId")}'
                f' host={message_queue.host}'
                f' queue_name={message_queue.queue_name}'
            )
