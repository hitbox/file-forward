import datetime

class OFPVersion:

    def __init__(self, datakey):
        self.datakey = datakey

    def __call__(self, data):
        return ofp_version(data[self.datakey])


class FlightDate:

    def __init__(self, day_key, month_abbr_key, abbr_year_key, assumed_year=2000):
        self.day_key = day_key
        self.month_abbr_key = month_abbr_key
        self.abbr_year_key = abbr_year_key
        self.assumed_year = assumed_year

    def __call__(self, data):
        day = data[self.day_key]
        month = month_from_abbr(data[self.month_abbr_key])
        year = self.assumed_year + data[self.abbr_year_key]
        return datetime.date(year, month, day)


class Schema:

    def __init__(self, keys_and_callables):
        self.keys_and_callables = keys_and_callables

    def __call__(self, data):
        result = {}
        for key, val in data.items():
            func = self.keys_and_callables[key]
            result[key] = func(val)
        # Call extra key function with typed data.
        for key, func in self.keys_and_callables.items():
            if key not in data:
                result[key] = func(result)
        return result


def month_from_abbr(string):
    return datetime.datetime.strptime(string, '%b').month

def int_or_none(value, none_value=None):
    if value is None:
        return none_value
    return int(str(value).strip())

def ofp_version(string, sep='_', fill='0'):
    parts = string.split(sep)
    while len(parts) < 3:
        parts.append(fill)
    return tuple(map(int, parts))
