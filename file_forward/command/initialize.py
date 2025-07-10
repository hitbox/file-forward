import logging

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from file_forward.configlib import add_config_option
from file_forward.model import Base
from file_forward.util import load_pyfile

logger = logging.getLogger(__name__)

def add_parser(argument_parser):
    """
    Add init sub-commands to parser.
    """
    init_command = argument_parser.add_parser(
        'init',
        help = 'Init commands.',
    )
    add_config_option(init_command)

    subparsers = init_command.add_subparsers()

    init_db_command = subparsers.add_parser(
        'db',
        help = 'Initialize database.',
    )
    init_db_command.set_defaults(func=init_db)
    add_config_option(init_db_command)
    init_db_command.add_argument('--seed', action='store_true')

def init_db(args):
    """
    Initialize and seed database.
    """
    appconfig = load_pyfile(args.config)

    database_uri = getattr(appconfig, 'SQLALCHEMY_DATABASE_URI')

    engine = create_engine(database_uri)
    Base.metadata.create_all(engine)

    if args.seed:
        seed_function = getattr(appconfig, 'seed', None)
        if seed_function:
            with Session(engine) as session:
                seed_function(session)
