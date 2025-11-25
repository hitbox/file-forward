from file_forward.configlib import add_config_option

from .from_logs import load_from_logs
from .from_schedule import load_from_schedule

def _add_load_from_schedule_parser(subparsers):
    # Load from OptiClimb schedule PDF files command.
    from_schedules_parser = subparsers.add_parser(
        'from_schedules',
        help = 'Load database models from OptiClimb schedule PDF files.',
    )
    add_config_option(from_schedules_parser)
    from_schedules_parser.set_defaults(func=load_from_schedule)

def _add_load_from_logs_parser(subparsers):
    # Load MessageCommitted instances from log files.
    from_logs_parser = subparsers.add_parser(
        'from_logs',
        help = 'Load data from log files.',
    )
    from_logs_parser.add_argument(
        'files',
        nargs = '+',
        help = 'Log files to parse and load MessageCommitted objects from.',
    )
    from_logs_parser.add_argument(
        '--commit',
        action = 'store_true',
        help = 'Commit the changes.',
    )
    add_config_option(from_logs_parser)
    from_logs_parser.set_defaults(func=load_from_logs)

def add_parser(argument_parser):
    """
    Add load sub-commands to parser.
    """
    load_command = argument_parser.add_parser(
        'load',
        help = 'Data loading commands.',
    )
    add_config_option(load_command)

    subparsers = load_command.add_subparsers()

    _add_load_from_schedule_parser(subparsers)
    _add_load_from_logs_parser(subparsers)
