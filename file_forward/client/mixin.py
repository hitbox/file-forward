import file_forward.util

class OSMixin:

    def normalize_path(self, path):
        return file_forward.util.normalize_path(path, posix=False)


class PosixMixin:

    def normalize_path(self, path):
        return file_forward.util.normalize_path(path, posix=True)
