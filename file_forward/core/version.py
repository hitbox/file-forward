class OFPVersion:
    """
    Parse OFP version strings.
    """

    def __init__(self, key, sep='_'):
        self.key = key
        self.sep = sep

    def __call__(self, data):
        string = data[self.key]
        parts = [int(num) for num in string.split('_')]
        while len(parts) < 3:
            parts.append(0)
        return tuple(parts)
