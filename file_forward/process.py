import logging

logger = logging.getLogger(__name__)

class Process:
    """
    Iterate files from scanner, write some output and archive file.
    """

    def __init__(
        self,
        scanner,
        archive,
        output,
        silent = False,
        database_uri = None,
    ):
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
        self.database_uri = database_uri

    def process_result(self, file_object):
        """
        Scrape and convert source data; write output; and archive.
        """
        logger.info('[%s]:%s', file_object.client.name, file_object.path)

        # Write output.
        self.output(file_object)

        # Add source to archive.
        self.archive.add(file_object)

    def __call__(self, process_name):
        """
        For each file produced by the scanner object, write some kind of output
        and archive.
        """
        for file_object in self.scanner:
            # Check if source already archived.
            if file_object not in self.archive:
                try:
                    self.process_result(file_object)
                except KeyboardInterrupt:
                    raise
                except Exception as exc:
                    logger.exception('An exception occurred.')
                    self.archive.handle_exception(file_object, exc)
                    if not self.silent:
                        raise

        # Save archive after all source files.
        self.archive.save()
