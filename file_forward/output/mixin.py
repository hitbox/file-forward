from operator import attrgetter

from file_forward.util import grouped
from file_forward.util import max_in_group

class AccumulateMixin:
    """
    Accumulate SourceResult objects and do all work on finalize.
    """

    def __call__(self, source_result):
        """
        Collect SourceResult objects into internal list.
        """
        if not hasattr(self, '_sources') or self._sources is None:
            self._sources = []

        self._sources.append(source_result)


class LegIdentifierMixin:
    """
    Mixin method to generate iterable of legs by newest OFP version.
    """

    _leg_identifier_key = attrgetter('leg_identifier')
    _ofp_version_key = attrgetter('ofp_version')

    def newest_by_ofp_version(self):
        """
        Generate only the newest OFP for each leg.
        """
        if hasattr(self, '_sources'):
            groupkey = self._leg_identifier_key
            newkey = self._ofp_version_key
            yield from max_in_group(self._sources, groupkey, newkey)
