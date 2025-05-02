import logging

from file_forward.lido import LCBMessage
from file_forward.util import decode_md
from file_forward.util import message_with_properties

from .base import OutputBase
from .mixin import AccumulateMixin
from .mixin import LegIdentifierMixin

logger = logging.getLogger(__name__)

class LCBOutput(
    AccumulateMixin,
    LegIdentifierMixin,
    OutputBase,
):
    """
    Write Lido LCB message to client.
    """

    def __init__(self, client, message_builder, context=None):
        """
        :param client:
            Message queue client.
        :param message_builder:
            Callable to build message for queue.
        :param context:
            Optional dict passed to LCBMessage.from_source_result.
        """
        self.client = client
        self.message_builder = message_builder
        self.context = context

    def put_message_jms(self, source_result):
        """
        Put message on queue with JMS keys.
        """
        data = source_result.zip_file_data()

        with self.client as message_queue:
            lcb_message = LCBMessage.from_source_result(
                source_result,
                self.context,
            )
            message_descriptor, put_message_options = message_with_properties(
                message_queue._queue_manager,
                lcb_message.get_fields(),
            )

            message_queue.put(data, message_descriptor, put_message_options)
            message_queue.commit()

            return message_descriptor

    def finalize(self):
        """
        Write the newest OFP by version to queue.
        """
        for source_result in self.newest_by_ofp_version():
            message_descriptor = self.put_message_jms(source_result)
            logger.info(
                'message committed:host=%r:queue_name=%r',
                self.client.host,
                self.client.queue_name,
            )
