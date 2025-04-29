import ftplib
import io

from file_forward.util import normalize_path

from .base import ClientBase

class FTPClient(ClientBase):

    def __init__(self, host, port, username, password):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self._ftp = None

    def _connect(self):
        self._ftp = ftplib.FTP()
        self._ftp.connect(self.host, self.port)
        self._ftp.login(self.username, self.password)

    def _close(self):
        self._ftp.quit()

    def __enter__(self):
        self._connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._close()

    def read(self, path, **kwargs):
        path = normalize_path(path, posix=True)
        stream = io.BytesIO()
        self._ftp.retrbinary(f'RETR {path}', stream.write)
        return stream.getvalue()

    def listdir(self, path=None):
        saved = None
        if path:
            path = normalize_path(path, posix=True)
            saved = self._ftp.pwd()
            self._ftp.cwd(path)
        result = self._ftp.nlst()
        if saved:
            self._ftp.cwd(saved)
        return result

    @property
    def name(self):
        return f'ftp:{self.username}@{self.host}'
