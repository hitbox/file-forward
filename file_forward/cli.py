import argparse

from file_forward import config

def main(argv=None):
    """
    Main command line entry point.
    """
    parser = argparse.ArgumentParser(
        description = '',
    )
    parser.add_argument(
        '--config',
    )
    args = parser.parse_args(argv)
    appconfig = config.load_pyfile(args.config)
    processes = getattr(appconfig, 'PROCESSES')

    for process_name, process in processes.items():
        print(process_name)
        print(process())
