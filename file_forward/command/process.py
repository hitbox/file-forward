import logging

from file_forward.util import load_pyfile

logger = logging.getLogger(__name__)

def add_parser(argument_parser):
    """
    Add process sub-command parser.
    """
    sub_command = argument_parser.add_parser(
        'process',
        help = process.__doc__,
    )
    sub_command.add_argument(
        '--config',
        help = 'Python config file.',
    )
    sub_command.set_defaults(func=process)

def process(args):
    """
    Run processes according to config.
    """
    appconfig = load_pyfile(args.config)
    processes = getattr(appconfig, 'PROCESSES')
    try:
        for process_name, process in processes.items():
            process(process_name)

        for process_name, process in processes.items():
            process.output.finalize()
    except KeyboardInterrupt:
        pass
    except:
        logger.exception('An exception occurred.')
