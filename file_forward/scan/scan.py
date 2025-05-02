import os
import re

from .base import ScanBase

from file_forward.model import SourceResult
from file_forward.util import strict_update

class Scan(ScanBase):
    """
    Match filenames against a pattern, scrape path and file data.
    """

    def __init__(
        self,
        client,
        pattern,
        root_dir,
        scrape = None,
        schema = None,
        posix = True,
    ):
        self.client = client
        self.pattern = pattern
        self.root_dir = root_dir
        self.scrape = scrape
        self.schema = schema
        self.posix = posix

    def generate_results(self):
        """
        Generate matching filenames produced from client and scrape data.
        """
        filename_re = re.compile(self.pattern)
        with self.client as client:
            for filename in client.listdir(self.root_dir):
                match = filename_re.match(filename)
                if match:
                    path = os.path.join(self.root_dir, filename)

                    # Scrape the path from regex capture groups, if any.
                    path_data = match.groupdict()

                    # Read data into memory.
                    file_data = client.read(path, mode='rb')

                    if self.scrape:
                        # Scrape file data, strictly adding more data.
                        scrape_data = self.scrape(file_data)
                        if not scrape_data:
                            raise ValueError('No data returned from scraper.')
                        # Update path_data, raising for existing keys.
                        strict_update(path_data, scrape_data)

                    if self.schema:
                        # Update types.
                        path_data = self.schema(path_data)

                    stat_data = self.client.stat(path)
                    source_result = SourceResult(self.client, path, path_data, file_data, stat_data, self.posix)
                    yield source_result
