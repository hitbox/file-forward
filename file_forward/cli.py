import argparse

from file_forward import config
from file_forward import runner
from file_forward.config import CONFIG_VAR

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

def main(argv=None):
    """
    Command line entry point.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)

    cp = config.from_args(args)

    named_items = [
        ('patterns', 'pattern.'),
        ('schemas', 'schema.'),
        ('sources', 'source.'),
    ]
    ic = config.InstantiateConfig(named_items)
    runconfig = ic(cp)

    from pprint import pprint
    for source_name, source in runconfig['sources'].items():
        for path, data in source.run():
            print(path)
            pprint(data)
