import paramiko

from .base import ClientBase

class SFTPClient(ClientBase):

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._transport = None
        self._sftp = None

    def _connect(self):
        """
        Update internal state to connected.
        """
        socket = (self.host, self.port)
        self._transport = paramiko.Transport(socket)
        self._transport.connect(
            username = self.username,
            password = self.password,
        )
        self._sftp = paramiko.SFTPClient.from_transport(self._transport)

    def _close(self):
        """
        Update internal state to closed.
        """
        self._sftp.close()
        self._transport.close()

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._close()

    def read(self, *args, **kwargs):
        with self._sftp.open(*args, **kwargs) as file:
            return file.read()

    def listdir(self, *args, **kwargs):
        return self._sftp.listdir(*args, **kwargs)

    @property
    def name(self):
        return f'sftp:{self.username}@{self.host}'
