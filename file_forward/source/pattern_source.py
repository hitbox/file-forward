import logging
import os
import re

from file_forward.util import strict_update

from .base import SourceBase
from .source_result import SourceResult

logger = logging.getLogger(__name__)

class PatternSource(SourceBase):
    """
    Match and parse regex against files in directory.
    """

    def __init__(self, pattern, root_dir, schema, scrape=None, posix=False):
        self.pattern = pattern
        self.root_dir = root_dir
        self.schema = schema
        self.scrape = scrape
        self.posix = posix

    def generate_results(self):
        filename_re = re.compile(self.pattern)
        for filename in os.listdir(self.root_dir):
            path = os.path.join(self.root_dir, filename)
            match = filename_re.match(filename)
            if match:
                # Read file data.
                with open(path, 'rb') as path_file:
                    file_data = path_file.read()

                # Scrape the path from regex capture groups, if any.
                path_data = match.groupdict()

                if self.scrape:
                    # Scrape file data, strictly adding more data.
                    scrape_data = self.scrape(file_data)
                    if not scrape_data:
                        raise ValueError('No data returned from scraper.')
                    strict_update(path_data, scrape_data)

                if self.schema:
                    # Update path data for types.
                    path_data = self.schema(path_data)

                source_result = SourceResult(filename, self.root_dir, path_data, file_data, self.posix)
                logger.info('file:%s', source_result.normalized_fullpath)
                yield source_result
