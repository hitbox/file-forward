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

    def process_result(self, source_result):
        """
        Scrape and convert source data; write output; and archive.
        """
        logger.info('[%s]:%s', source_result.client.name, source_result.path)

        # Write output.
        self.output(source_result)

        # Add source to archive.
        self.archive.add(source_result)

    def __call__(self, process_name):
        """
        For each source_result produced by the `source` object, write some kind
        of output and archive.
        """
        logger.info('begin %s', process_name)
        processed = 0
        exceptions = 0

        for source_result in self.scanner:
            # Check if source already archived.
            if source_result not in self.archive:
                try:
                    self.process_result(source_result)
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    logger.exception('An exception occurred.')
                    self.archive.handle_exception(source_result, exc)
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
