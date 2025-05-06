import logging

logger = logging.getLogger(__name__)

class Process:
    """
    """

    def __init__(self, scanner, archive, output, silent=False):
        """
        :param scanner:
            Iterable object that produces `SourceResult` objects.
        :param archive:
            Archive object that checks if `SourceResult` objects have already
            been processed and saves them after processing.
        :param output:
            Callable object that writes output for unprocessed source result objects.
        :param silent:
            If False, raise after logging exceptions.
        """
        self.scanner = scanner
        self.archive = archive
        self.output = output
        self.silent = silent

    def process_result(self, file):
        """
        Scrape and convert source data; write output; and archive.
        """
        logger.info('[%s]:%s', file.client.name, file.path)

        # Write output.
        self.output(file)

        # Add source to archive.
        self.archive.add(file)

    def __call__(self, process_name):
        """
        For each file produced by the scanner object, write some kind of output
        and archive.
        """
        logger.info('begin %s', process_name)
        processed = 0
        exceptions = 0

        for file in self.scanner:
            # TODO
            # - Avoid scraping and processing in scanner just to throw it away
            #   in here.

            # Check if source already archived.
            if file not in self.archive:
                try:
                    self.process_result(file)
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    logger.exception('An exception occurred.')
                    self.archive.handle_exception(file, exc)
                    exceptions += 1
                    if not self.silent:
                        raise
                else:
                    # Success
                    processed += 1

        # Save archive after all source files.
        self.archive.save()

        logger.info(
            '%s processed %s with %s exceptions',
            process_name, processed, exceptions)
