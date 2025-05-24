from sqlalchemy import create_engine

from file_forward.util import load_pyfile

def add_config_option(parser):
    """
    Add very common command line option for config.
    """
    parser.add_argument(
        '--config',
        help = 'Python config file.',
    )

def engine_from_config(appconfig):
    """
    Parse config from arguments and return engine.
    """
    database_uri = getattr(appconfig, 'SQLALCHEMY_DATABASE_URI')
    engine = create_engine(database_uri)
    return engine
