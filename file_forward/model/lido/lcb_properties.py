from collections import namedtuple

from .base import LidoBase
from .lido_meta_property import LidoMetaProperty

class LCBProperties(
    namedtuple(
        'LCBProperties',
        field_names = [
            'lido_meta',
            'lido_application_id',
            'lido_business_id',
            'lido_client_id',
            'lido_customer_id',
            'lido_leg_identifier',
            'lido_msg_version',
            'lido_time_stamp',
            'lido_trace_id',
        ],
        defaults = [
            # Everything except lido_meta.
            None, # lido_application_id
            None, # lido_business_id
            None, # lido_client_id
            None, # lido_customer_id
            None, # lido_leg_identifier
            None, # lido_msg_version
            None, # lido_time_stamp
            None, # lido_trace_id
        ],
    ),
    LidoBase,
):
    """
    :param lido_meta:
        This mandatory property with crucial information for proper adding,
        replacing or removing documents to the correct briefing package.
        Detailed description below. JSON document.
    """

    field_types = {
        'lido_meta': LidoMetaProperty,
    }

    @classmethod
    def from_source_result(cls, source_result, context=None):
        return cls(
            lido_meta = LidoMetaProperty.from_source_result(source_result, context),
        )

