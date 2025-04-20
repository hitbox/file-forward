import datetime
import re

class FlightDate:
    """
    Convert incomplete date string to datetime.date.
    """

    def __init__(self, day_key, month_abbr_key, abbr_year_key, assumed_year=2000):
        self.day_key = day_key
        self.month_abbr_key = month_abbr_key
        self.abbr_year_key = abbr_year_key
        self.assumed_year = assumed_year

    def __call__(self, data):
        day = data[self.day_key]
        month = datetime.datetime.strptime(data[self.month_abbr_key], '%b').month
        year = self.assumed_year + data[self.abbr_year_key]
        return datetime.date(year, month, day)


class Schema:
    """
    Apply callables data, to convert their type.
    """

    def __init__(self, keys_and_callables):
        self.keys_and_callables = keys_and_callables

    def __call__(self, data):
        result = {}
        # Call for each key from source data.
        for key, val in data.items():
            func = self.keys_and_callables[key]
            result[key] = func(val)
        # Call extra key function with typed data.
        for key, func in self.keys_and_callables.items():
            if key not in data:
                result[key] = func(result)
        return result
