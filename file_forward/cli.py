import argparse

from file_forward import command

def argument_parser():
    """
    Return argument parser.
    """
    parser = argparse.ArgumentParser(
        prog = 'file_forward',
        description =
            'Process files from sources and, primarily,'
            ' send to a IBM MQ queue.',
    )
    command.add_parsers(parser.add_subparsers())
    return parser

def main(argv=None):
    """
    Main command line entry point.
    """
    parser = argument_parser()
    args = parser.parse_args(argv)
    func = args.func
    delattr(args, 'func')
    func(args)
