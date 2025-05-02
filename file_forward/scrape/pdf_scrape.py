import contextlib
import io
import os
import re

import pdfplumber

from file_forward.util import strict_update

from .base import ScrapeBase

class PDFScrape(ScrapeBase):
    """
    Scrape the `from` and `to` (as destination) fields from OptiClimb PDF files.
    """

    def __init__(self, *regexes, raise_for_empty=True):
        self.regexes = tuple(map(re.compile, regexes))
        self.raise_for_empty = raise_for_empty

    def _data_from_pdf(self, pdf):
        """
        Scrape data with a regex from a PDF for each line of each page.
        """
        data = {}
        # Apply regex to each line of each page and update data for matches.
        for page in pdf.pages:
            page_text = page.extract_text()
            for line in page_text.splitlines():
                for regex in self.regexes:
                    match = regex.match(line)
                    if match:
                        strict_update(data, match.groupdict())
        return data

    def __call__(self, pdf_bytes):
        """
        Loop through the pdf pages and search lines for matches against regex.
        """
        pdf_stream = io.BytesIO(pdf_bytes)
        # Silence pdfplumber
        with contextlib.redirect_stderr(open(os.devnull, 'w')):
            with pdfplumber.open(pdf_stream) as pdf:
                data = self._data_from_pdf(pdf)
                if not data and self.raise_for_empty:
                    raise ValueError('No data scraped for PDF.')
        return data


opticlimb_pdf_scraper = PDFScrape(
    # Find matching line to get destination_icao.
    r'A/C : (?P<aircraft_registration>[A-Z0-9]{1,6})'
    r' From : [A-Z]{4}'
    r' To : (?P<destination_icao>[A-Z]{4})',
)
