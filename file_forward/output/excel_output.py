import logging

from openpyxl import Workbook
from openpyxl.styles import Font

from .base import OutputBase
from .mixin import AccumulateMixin
from .mixin import LegIdentifierMixin

logger = logging.getLogger(__name__)

class ExcelOutput(
    AccumulateMixin,
    LegIdentifierMixin,
    OutputBase,
):
    """
    Assemble source objects into an Excel report.
    """

    def __init__(
        self,
        filename,
        rowifier,
        freeze_first_row = False,
        autofilter = False,
        filters = None,
    ):
        """
        :param filename:
            Workbook filename to save.
        :param rowifier:
            Callable object to convert an iterable of dicts into (values,
            classes) with which to format and write to Excel.
        :param freeze_first_row:
            Freeze the worksheet's top (header) row.
        :param autofilter:
            Apply auto filter to worksheet.
        """
        self.filename = filename
        self.rowifier = rowifier
        self.freeze_first_row = freeze_first_row
        self.autofilter = autofilter
        self.filters = filters
        self._sources = None

    def add_autofilter(self, ws):
        ws.auto_filter.ref = ws.dimensions
        if self.filters:
            for column_index, filter_values in self.filters:
                if callable(filter_values):
                    filter_values = filter_values(ws, column_index)
                ws.auto_filter.add_filter_column(column_index, filter_values)

    def finalize(self):
        """
        Write information about newest leg identifiers by OFP version to Excel
        workbook.
        """
        wb = Workbook()
        ws = wb.active

        if self.freeze_first_row:
            ws.freeze_panes = 'A2'

        data_rows = [source.flat_dict() for source in self.newest_by_ofp_version()]
        for values, classes in self.rowifier(data_rows):
            ws.append(values)
            if 'header' in classes:
                for cell in ws[ws.max_row]:
                    cell.font = Font(bold=True)

        if self.autofilter:
            self.add_autofilter(ws)

        wb.save(self.filename)
        logger.info('saved %s', self.filename)
