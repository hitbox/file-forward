import logging

from file_forward.model.lido import LCBMessage
from file_forward.util import message_with_properties
from file_forward.util import zip_bytes

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

    def __init__(self, client, context=None):
        """
        :param client:
            Message queue client.
        :param context:
            Optional dict passed to LCBMessage.from_source_result.
        """
        self.client = client
        self.context = context

    def put_message_jms(self, file):
        """
        Put message on queue with JMS keys.
        """
        data = zip_bytes(file.file_data, file.filename)

        with self.client as message_queue:
            lcb_message = LCBMessage.from_source_result(
                file,
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
        for file in self.newest_by_ofp_version():
            message_descriptor = self.put_message_jms(file)
            logger.info(
                'message committed:host=%r:queue_name=%r',
                self.client.host,
                self.client.queue_name,
            )
