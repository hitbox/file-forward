import json
import logging

import pymqi

from file_forward.lido import LCBMessage
from file_forward.util import decode_md
from file_forward.util import message_with_properties

from .base import OutputBase

logger = logging.getLogger(__name__)

class LCBOutput(OutputBase):
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

    def put_message(self, source_result):
        message = self.message_builder(source_result)
        with self.client as message_queue:
            message_descriptor = message_queue.put(message)
            message_queue.commit()
            return message_descriptor

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

    def log(self, message_descriptor):
        # Log resulting message descriptor.
        logger.info(
            'message committed:host=%r:queue_name=%r',
            self.client.host,
            self.client.queue_name,
        )

    def __call__(self, source_result):
        """
        Put message on queue.
        """
        message_descriptor = self.put_message_jms(source_result)
        self.log(message_descriptor)
