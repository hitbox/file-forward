from collections import namedtuple

class OFPVersion(
    namedtuple(
        'OFPVersion',
        field_names = [
            'ofp_version_major',
            'ofp_version_minor',
            'ofp_version_patch',
        ],
        defaults = [
            0,
            0,
            0,
        ],
    ),
):
    """
    Named tuple of the three parts of an OFP version--the major, minor, and patch integers.
    """
