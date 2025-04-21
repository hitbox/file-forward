import datetime

class Schema:
    """
    Run callables against existing data keys and then run extra keys against
    the first result, creating new keys.
    """

    def __init__(self, keys_and_callables):
        self.keys_and_callables = keys_and_callables

    def __call__(self, data):
        result = {}
        # Convert or validate existing keys.
        for key, val in data.items():
            func = self.keys_and_callables[key]
            result[key] = func(val)
        # Call extra key function with typed data.
        for key, func in self.keys_and_callables.items():
            if key not in data:
                result[key] = func(result)
        return result


class Date:
    """
    Convert date string to datetime.date.
    """

    def __init__(self, key, format_string):
        self.key = key
        self.format_string = format_string

    def __call__(self, data):
        value = data[self.key]
        dt = datetime.datetime.strptime(data[self.key], self.format_string)
        return dt.date()


class OFPVersion:
    """
    Convert string from regex captured data into OFP version tuple.
    """

    def __init__(self, datakey, sep='_', fill='0'):
        self.datakey = datakey
        self.sep = sep
        self.fill = fill

    def __call__(self, data):
        string = data[self.datakey]
        parts = string.split(self.sep)
        while len(parts) < 3:
            parts.append(self.fill)
        return tuple(map(int, parts))


def int_or_none(value, none_value=None):
    if value is None:
        return none_value
    return int(str(value).strip())
