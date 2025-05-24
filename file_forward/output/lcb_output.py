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
    Write Lido LCB message to client. Files are collected into a list
    (AccumulateMixin) and sorted by OFP version (LegIdentifierMixin).
    """

    def __init__(
        self,
        client,
        filter_func,
        context = None,
    ):
        """
        :param client:
            Message queue client.
        :param filter_func:
            Callable takes lcb_message and returns True to send message.
        :param context:
            Optional dict passed to LCBMessage.from_source_result.
        """
        self.client = client
        self.filter_func = filter_func
        self.context = context

    def put_message_jms(self, fields, data):
        """
        Put message on queue with JMS keys.
        """
        with self.client as message_queue:
            message_descriptor, put_message_options = message_with_properties(
                message_queue._queue_manager,
                fields,
            )

            message_queue.put(data, message_descriptor, put_message_options)
            message_queue.commit()

            return message_descriptor

    def finalize_file(self, file_object):
        """
        Create LCB message and save database object; and optionally send
        message.
        """
        data = zip_bytes(file_object.file_data, file_object.filename)
        lcb_message = LCBMessage.from_source_result(file_object, self.context)

        # Want to know which message were sent.
        # Make database objects for all with a column for sent_at or something.
        # Output objects accumulate files so they can sort for newest ofp.
        # Let this and the archive both try to make the database objects?
        message_fields = lcb_message.get_fields()

        # Filter function decides if message is sent.
        if self.filter_func(lcb_message):
            # Send JMS message.
            message_descriptor = self.put_message_jms(message_fields, data)
            logger.debug(
                'message committed:host=%s:queue=%s:fields=%s',
                self.client.host, self.client.queue_name, message_fields)
        else:
            # Log message not sent.
            logger.debug('fields rejected by filter: %s', message_fields)

    def finalize(self):
        """
        Write the newest OFP by version to queue.
        """
        for file_object in self.newest_by_ofp_version():
            self.finalize_file(file_object)
