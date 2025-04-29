from collections import namedtuple

from .base import LidoBase

DEFAULT_OPERATIONAL_SUFFIX = 'L'

class LegIdentifierField(
    namedtuple(
        'LegIdentifierField',
        field_names = [
            'airline_code',
            'flight_number',
            'date_of_origin',
            'departure_airport',
            'destination_airport',
            'operational_suffix',
        ],
        defaults = [
            DEFAULT_OPERATIONAL_SUFFIX,
        ],
    ),
    LidoBase,
):
    """
    Value for LidoMeta JSON to identify flight to upload file for. It is always
    a string for output.
    """

    __formatters__ = {
        'date_of_origin': lambda date: date.strftime('%d%b%Y'),
    }

    # Rename scraped data to match this class' keyword arguments.
    _opticlimb_key_map = {
        'airline_iata': 'airline_code',
        'flight_date': 'date_of_origin',
        'departure_iata': 'departure_airport',
        'destination_iata': 'destination_airport',
    }

    @classmethod
    def from_source_result(cls, source_result, context):
        return cls.from_opticlimb(source_result.path_data, context)

    @classmethod
    def from_opticlimb(cls, data, context):
        """
        LegIdentifierField from scraped and typed OptiClimb data.
        """
        # Rename for keywords.
        renamed = {cls._opticlimb_key_map.get(key, key): val for key, val in data.items()}
        # Filter for only expected keywords.
        kwargs = {key: val for key, val in renamed.items() if key in cls._fields}
        return cls(**kwargs)

    def _value(self, key):
        """
        Get and format the value for key.
        """
        value = getattr(self, key)
        if key in self.__formatters__:
            # Format value from callable.
            value = self.__formatters__[key](value)
        return value

    def _as_string(self, sep='.'):
        """
        Format leg identifier as the character separated string, that the
        LidoMeta property/element expects.
        """
        # Filter keys for None values.
        keys = (key for key in self._fields if getattr(self, key) is not None)
        # Resolve keys' values.
        values = map(self._value, keys)
        # Convert to string and join on sep.
        return sep.join(map(str, values))

    def __str__(self):
        return self._as_string()
