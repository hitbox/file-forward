import ftplib
import io
import posixpath
import time

from ftplib import error_perm
from types import SimpleNamespace

from file_forward.util import posix_parts

from .base import ClientBase
from .mixin import PosixMixin

class FTPClient(PosixMixin, ClientBase):

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
        path = self.normalize_path(path)
        stream = io.BytesIO()
        self._ftp.retrbinary(f'RETR {path}', stream.write)
        return stream.getvalue()

    def listdir(self, path=None):
        saved = None
        if path:
            path = self.normalize_path(path)
            saved = self._ftp.pwd()
            self._ftp.cwd(path)
        result = self._ftp.nlst()
        if saved:
            self._ftp.cwd(saved)
        return result

    def exists(self, path):
        # Try for files
        try:
            self._ftp.size(path)
            return True
        except error_perm as e:
            if not str(e).startswith('550'):
                raise

        # Try for directories
        current = self._ftp.pwd()
        try:
            self._ftp.cwd(path)
            self._ftp.cwd(current)
            return True
        except error_perm as e:
            if not str(e).startswith('550'):
                raise

        return False

    def move(self, src, dst):
        self._ftp.rename(src, dst)

    def makedirs(self, path):
        parts = posix_parts(path)
        path = ''
        for part in parts:
            path = posixpath.join(path, part)
            try:
                self._ftp.cwd(path)
            except:
                self._ftp.mkd(path)
                self._ftp.cwd(path)

    def stat(self, path):
        path = self.normalize_path(path)
        mtime_string = self._ftp.sendcmd(f'MDTM {path}')[4:].strip()
        mtime_struct = time.strptime(mtime_string, '%Y%m%d%H%M%S')
        mtime = time.mktime(mtime_struct)

        stat = SimpleNamespace(st_mtime=mtime, st_atime=mtime)
        return stat

    @property
    def name(self):
        return f'ftp:{self.username}@{self.host}'
