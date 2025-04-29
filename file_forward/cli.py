import argparse
import logging

from file_forward.util import load_pyfile

logger = logging.getLogger(__name__)

def argument_parser():
    """
    Return argument parser.
    """
    parser = argparse.ArgumentParser(
        description =
            'Process files from sources and, primarily,'
            ' send to a IBM MQ queue.',
    )
    parser.add_argument(
        '--config',
        help = 'Python config file. Must provide PROCESSES.',
    )
    return parser

def main(argv=None):
    """
    Main command line entry point.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)
    appconfig = load_pyfile(args.config)
    processes = getattr(appconfig, 'PROCESSES')

    try:
        for process_name, process in processes.items():
            process(process_name)
    except KeyboardInterrupt:
        pass
    else:
        logger.info('finished')
