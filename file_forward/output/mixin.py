from operator import itemgetter

from file_forward.constant import LEG_IDENTIFIER_KEYS
from file_forward.constant import OFP_VERSION_KEYS
from file_forward.util import grouped
from file_forward.util import max_in_group

leg_identifier_key = itemgetter(*LEG_IDENTIFIER_KEYS)
ofp_version_key = itemgetter(*OFP_VERSION_KEYS)

class AccumulateMixin:
    """
    Accumulate SourceResult objects and do all work on finalize.
    """

    def __call__(self, source_result):
        """
        Collect SourceResult objects into internal list.
        """
        if not hasattr(self, '_sources') or self._sources is None:
            # Initialize _sources list.
            self._sources = []

        self._sources.append(source_result)


class LegIdentifierMixin:
    """
    Mixin method to generate iterable of legs by newest OFP version.
    """

    @staticmethod
    def _leg_identifier_key(file):
        return leg_identifier_key(file.path_data)

    @staticmethod
    def _ofp_version_key(file):
        return ofp_version_key(file.path_data)

    def newest_by_ofp_version(self):
        """
        Generate only the newest OFP for each leg.
        """
        if hasattr(self, '_sources'):
            groupkey = self._leg_identifier_key
            newkey = self._ofp_version_key
            yield from max_in_group(self._sources, groupkey, newkey)
