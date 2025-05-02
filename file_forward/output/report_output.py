import csv

from file_forward.util import strict_update

from .base import OutputBase

class ReportOutput(OutputBase):
    """
    Accumulate source objects and create a report.
    """

    def __init__(self, output, header, formatters=None, message_builder=None):
        self.output = output
        self.header = header
        if formatters is None:
            formatters = {}
        self.formatters = formatters
        self.message_builder = message_builder
        self._sources = []

    def __call__(self, source_result):
        self._sources.append(source_result)

    def finalize(self):
        """
        Create a report from accumulated source objects.
        """
        source_attrs = ['client_name', 'normalized_fullpath', 'path_data']

        def formatted(key, val):
            if key in self.formatters:
                val = self.formatters[key](val)
            return val

        with open(self.output, mode='w', newline='', encoding='utf8') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=self.header)
            writer.writeheader()

            for source in self._sources:
                source_data = {}
                for attr in source_attrs:
                    value = getattr(source, attr)
                    if not isinstance(value, dict):
                        value = {attr: value}
                    strict_update(source_data, value)

                row = {k: formatted(k, v) for k, v in source_data.items() if k in self.header}
                writer.writerow(row)
