import argparse
import logging

from file_forward import config

logger = logging.getLogger(__name__)

def argument_parser():
    parser = argparse.ArgumentParser(
        description = '',
    )
    parser.add_argument(
        '--config',
    )
    return parser

def main(argv=None):
    """
    Main command line entry point.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)
    appconfig = config.load_pyfile(args.config)
    processes = getattr(appconfig, 'PROCESSES')

    try:
        for process_name, process in processes.items():
            process(process_name)
    except KeyboardInterrupt:
        pass
    else:
        logger.info('finished')
