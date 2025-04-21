import sys

from abc import ABC
from abc import abstractmethod
from pprint import pprint

class OutputBase(ABC):

    @abstractmethod
    def __call__(self, source_result):
        """
        Write output from source result object.
        """


class FileOutput(OutputBase):
    # XXX: WIP

    def __init__(self, stream=None):
        if stream is None:
            stream = sys.stdout
        self.stream = stream

    def __call__(self, source_result):
        print(source_result.ppstring())


class MQOutput(OutputBase):
    """
    Write message to IBM MQ queue.
    """
    # XXX: WIP

    def __init__(self, client):
        self.client = client

    def __call__(self, source_result):
        """
        Write message to IBM MQ queue.
        """
        with self.client as mq:
            message_descriptor = mq.put('Hello from file-forward.')
            mq.commit()
            print(message_descriptor)
