import getpass
import os
import shutil
import socket

from .base import ClientBase
from .mixin import OSMixin

class OSClient(OSMixin, ClientBase):

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

    def exists(self, path):
        return os.path.exists(path)

    def move(self, src, dst):
        return shutil.move(src, dst)

    def makedirs(self, path):
        os.makedirs(path)

    def stat(self, path):
        return os.stat(path)

    @property
    def name(self):
        return f'local:{self.username}@{self.hostname}'
