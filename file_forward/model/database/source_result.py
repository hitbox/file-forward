import os

from collections import namedtuple

from file_forward.util import strict_update

class SourceResult(
    namedtuple(
        'SourceResult',
        field_names = [
            'client',
            'path',
            'path_data',
            'file_data',
            'stat_data',
        ],
    ),
):
    """
    Consistent object for result of source objects.
    """
    # TODO
    # - Replace this class with `file_forward.model.File` and persist.

    @property
    def filename(self):
        return os.path.basename(self.path)

    def flat_dict(self):
        """
        Flattened data dict for use in format strings.
        """
        data = {
            'client_name': self.client.name,
            'path': self.path,
        }
        strict_update(data, self.path_data)
        return data
