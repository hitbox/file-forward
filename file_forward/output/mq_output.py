import logging

from file_forward.util import decode_md

from .base import OutputBase
from .mixin import AccumulateMixin
from .mixin import LegIdentifierMixin

logger = logging.getLogger(__name__)

class MQOutput(
    AccumulateMixin,
    LegIdentifierMixin,
    OutputBase,
):
    """
    Write message to IBM MQ queue.
    """
    # Sending PDF inside ZIP to Lido LCB.

    def __init__(self, client):
        self.client = client

    def finalize(self):
        with self.client as message_queue:
            for source in self.newest_by_ofp_version():
                message_descriptor = message_queue.put(source_result.file_data)
                message_queue.commit()

                # Decode message after server does things to it, and log.
                md_data = decode_md(message_descriptor)
                logger.info(
                    'message committed.'
                    f' MsgId={md_data.get("MsgId")}'
                    f' host={message_queue.host}'
                    f' queue_name={message_queue.queue_name}'
                )
