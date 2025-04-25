import sys

from file_forward.util import writer

from .base import OutputBase

class FileOutput(OutputBase):
    # XXX: WIP

    def __init__(self, stream=None):
        self.stream = stream

    def __call__(self, source_result):
        print(source_result.ppstring(), file=writer(self.stream))
