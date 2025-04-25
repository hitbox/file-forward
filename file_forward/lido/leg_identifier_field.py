class LegIdentifierField:

    keys = [
        'airline_code',
        'flight_number',
        'date_of_origin',
        'departure_airport',
        'destination_airport',
        'operational_suffix',
    ]

    formatters = {
        'date_of_origin': lambda date: date.strftime('%d%b%Y'),
    }

    def __init__(
        self,
        airline_code,
        flight_number,
        date_of_origin,
        departure_airport,
        destination_airport,
        operational_suffix = None,
    ):
        self.airline_code = airline_code
        self.flight_number = flight_number
        self.date_of_origin = date_of_origin
        self.departure_airport = departure_airport
        self.destination_airport = destination_airport
        self.operational_suffix = operational_suffix

    @classmethod
    def from_opticlimb(cls, data):
        """
        LegIdentifierField from scraped OptiClimb data.
        """
        # Expecting typed data.
        return cls(
            airline_code = data['airline_iata'],
            flight_number = data['flight_number'],
            date_of_origin = data['flight_date'],
            departure_airport = data['departure_iata'],
            destination_airport = data['destination_iata'],
            operational_suffix = data.get('operational_suffix'),
        )

    def _value(self, key):
        value = getattr(self, key)
        if key in self.formatters:
            value = self.formatters[key](value)
        return value

    def as_string(self, sep='.'):
        """
        """
        # Filter keys for not None values.
        keys = (key for key in self.keys if getattr(self, key, None) is not None)
        # Resolve keys' values.
        values = (self._value(key) for key in keys)
        # Convert to string and join on sep.
        return sep.join(map(str, values))
