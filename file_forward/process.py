import logging

logger = logging.getLogger(__name__)

class Process:
    """
    Take source files that have not been archived and write some kind of
    output; and save the path as processed.
    """

    def __init__(self, source, archive, output, save_per_file=True):
        """
        :param source:
            Iterable object that produces `SourceResult` objects.
        :param archive:
            Archive object that checks if `SourceResult` objects have already
            been processed and saves them after processing.
        :param output:
            Callable object that writes output for unprocessed source objects.
        :param save_per_file:
            If True (default) commit archive object for every source object.
        """
        self.source = source
        self.archive = archive
        self.output = output
        self.save_per_file = save_per_file

    def __call__(self, process_name):
        """
        For each source_result produced by the `source` object, write some kind
        of output and archive.
        """
        for source_result in self.source:
            # Check if source already archived.
            if source_result in self.archive:
                continue

            # Write output.
            self.output(source_result)

            # Add source to archive.
            self.archive.add(source_result)

            if self.save_per_file:
                # Save archive after every source file.
                self.archive.save()

        if not self.save_per_file:
            # Save archive after all source files.
            self.archive.save()

        logger.info('%s finished', process_name)
