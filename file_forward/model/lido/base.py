import json
import xml.etree.ElementTree as ET

from file_forward.util import jsonable

class LidoBase:

    field_types = {}

    @classmethod
    def from_source_result(cls, source_result, context=None):
        """
        """
        if cls is LidoBase:
            raise TypeError(
                f'{cls} from_source_result not intended to create LidoBase objects.')

        def get_value(key):
            if key in cls.field_types:
                type_ = cls.field_types[key]
                if hasattr(type_, 'from_source_result'):
                    value = type_.from_source_result(source_result, context)
                else:
                    value = type_()
            return value

        kwargs = {key: get_value(key) for key, type_ in cls.field_types.items()}
        return cls(**kwargs)
