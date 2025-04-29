import getpass
import os
import socket

from .base import ClientBase

class OSClient(ClientBase):

    def __init__(self):
        self.username = getpass.getuser()
        self.hostname = socket.gethostname()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def read(self, *args, **kwargs):
        with open(*args, **kwargs) as file:
            return file.read()

    def listdir(self, *args, **kwargs):
        return os.listdir(*args, **kwargs)

    @property
    def name(self):
        return f'local:{self.username}@{self.hostname}'
