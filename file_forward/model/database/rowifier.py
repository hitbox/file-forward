class Rowifier:
    """
    List of dicts to rows for Excel formatting hints through class names.
    """

    def __init__(self, header, include_header=True, formatters=None):
        """
        :param header:
            The order of keys to get from the dicts.
        :param include_header:
            Include a header row in generated output.
        :param formatters:
            Dict of keys to callables to format values.
        """
        self.header = header
        self.include_header = include_header
        self.formatters = {} if formatters is None else formatters

    def __call__(self, rows):
        """
        Generate an item (values, classes) for Excel output to use.
        """
        if self.include_header:
            values = tuple(self.header)
            classes = set(['header'])
            yield (values, classes)

        # Pass-through value (no formatter).
        pass_value = lambda value: value

        # Formatter for key or pass-through.
        formatter = lambda key: self.formatters.get(key, pass_value)

        for row_data in rows:
            values = tuple(formatter(key)(row_data[key]) for key in self.header)
            classes = set(['data'])
            yield (values, classes)
