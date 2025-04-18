import configparser
import os

from .const import CONFIG_VAR

def from_args(args):
    """
    Return config parser from command line arguments.
    """
    cp = configparser.ConfigParser()

    if args.config:
        # Read from command line arguments.
        for filename in args.config:
            if not os.path.exists(filename):
                raise FileNotFoundError(f'Config not found {filename!r}')
        cp.read(args.config)
    elif CONFIG_VAR in os.environ:
        # Read optional environment variable.
        filename = os.environ[CONFIG_VAR]
        if not os.path.exists(filename):
            raise FileNotFoundError(f'Config not found {filename!r}')
        cp.read(filename)
    else:
        raise ValueError('Unable to find configuration files.')

    return cp
