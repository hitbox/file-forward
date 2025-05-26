import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from file_forward import context
from file_forward.configlib import add_config_option
from file_forward.configlib import engine_from_config
from file_forward.model import Base
from file_forward.model import File
from file_forward.model import LCBMessageModel
from file_forward.util import load_pyfile

logger = logging.getLogger(__name__)

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

    # Load from OptiClimb schedule PDF files command.
    load_from_schedule_command = subparsers.add_parser(
        'schedule_pdf',
        help = 'Load database models from OptiClimb schedule PDF files.',
    )
    add_config_option(load_from_schedule_command)
    load_from_schedule_command.set_defaults(func=load_from_schedule)

def load_from_schedule(args):
    """
    Load OptiClimb schedule PDF files as database objects.
    """
    appconfig = load_pyfile(args.config)
    engine = engine_from_config(appconfig)

    with Session(engine) as session:
        context.set_session_context(session)

        scanner = appconfig.local_schedule_pdf_scan

        for file_obj in scanner.generate_results():

            file_instance = File.from_source_result(file_obj)

            token = context.extra_data.set(file_obj.path_data)
            try:
                lcb_message_instance = LCBMessageModel.from_source_result(file_obj)
            finally:
                context.extra_data.reset(token)

            lcb_message_instance.file = file_instance

            session.add(lcb_message_instance)

        session.commit()
