import json
import xml.etree.ElementTree as ET

from file_forward.util import jsonable

class LidoBase:

    field_types = {}

    @classmethod
    def from_source_result(cls, source_result):
        """
        """
        if cls is LidoBase:
            raise TypeError(f'{cls} from_source_result not intended to create LidoBase objects.')

        def value(key):
            if key in cls.field_types:
                val = cls.field_types[key]
                if hasattr(val, 'from_source_result'):
                    val = val.from_source_result(source_result)
                else:
                    val = val()
            return val

        kwargs = {key: value(key) for key, type_ in cls.field_types.items()}
        return cls(**kwargs)
