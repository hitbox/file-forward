import argparse
import re

from file_forward import config
from file_forward import core
from file_forward import runner
from file_forward.config import CONFIG_VAR
from file_forward.config.instance import InstanceConfig

def argument_parser():
    """
    Argument parser.
    """
    parser = argparse.ArgumentParser(
        description = runner.run.__doc__,
    )
    parser.add_argument(
        '--config',
        action = 'append',
        default = [],
        help =
            'Configuration files. Environment variable'
            f' {CONFIG_VAR} is also loaded.',
    )
    return parser

def get_runconfig(cp):
    ic = InstanceConfig(
        named_items = [
            ('patterns', 'pattern.'),
            ('schemas', 'schema.'),
            ('sources', 'source.'),
        ],
        get_context = lambda: {
            'str': str,
            'int': int,
            're': re,
            **core._context(),
        },
    )
    runconfig = ic(cp)
    return runconfig

def main(argv=None):
    """
    Command line entry point.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)

    cp = config.from_args(args)
    runconfig = get_runconfig(cp)

    from pprint import pprint
    for source_name, source in runconfig['sources'].items():
        for path, data in source.run():
            print(path)
            pprint(data)
