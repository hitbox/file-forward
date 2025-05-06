from collections import namedtuple

from .base import LidoBase

class LCBHeader(
    namedtuple(
        'LCBHeader',
        field_names = [
            'jms_expiration',
            'jms_type',
        ],
        defaults = [
            None, # jms_expiration
            'Byte', # jms_type
        ],
    ),
    LidoBase,
):
    """
    :param jms_type:
        Documents in payload will be sent in binary format (ZIP archive).
        Default fixed value: Byte
    :jms_expiration:
        Contains message’s expiration timestamp in milliseconds. Default
        expiration is set to 24h.
        Sample: 1546344000000
    """
