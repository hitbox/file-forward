import argparse
import configparser
import datetime
import fnmatch
import inspect
import os
import re

from contextlib import contextmanager

import paramiko

APP = 'file_forward'
CONFIG_VAR = 'FILE_FORWARD_CONFIG'

class RegexSchema:

    def __init__(self, pattern, schema):
        self.pattern = pattern
        self.schema = schema

    def match(self, *args):
        return re.match(*args)


class FlightDate:

    def __init__(self, day_key, month_abbr_key, abbr_year_key, assumed_year=2000):
        self.day_key = day_key
        self.month_abbr_key = month_abbr_key
        self.abbr_year_key = abbr_year_key
        self.assumed_year = assumed_year

    def __call__(self, data):
        day = data[self.day_key]
        month = datetime.datetime.strptime(data[self.month_abbr_key], '%b').month
        year = self.assumed_year + data[self.abbr_year_key]
        return datetime.date(year, month, day)

class Schema:

    def __init__(self, keys_and_callables):
        self.keys_and_callables = keys_and_callables

    def __call__(self, data):
        result = {}
        for key, val in data.items():
            func = self.keys_and_callables[key]
            result[key] = func(val)
        # Call extra key function with typed data.
        for key, func in self.keys_and_callables.items():
            if key not in data:
                result[key] = func(result)
        return result


class PatternSource:

    def __init__(self, pattern, root_dir, schema):
        self.pattern = pattern
        self.root_dir = root_dir
        self.schema = schema

    def run(self):
        filename_re = re.compile(self.pattern)
        for filename in os.listdir(self.root_dir):
            path = os.path.join(self.root_dir, filename)
            match = filename_re.match(filename)
            if match:
                data = self.schema(match.groupdict())
                yield (path, data)


class SFTPGlob:
    """
    Iterator of paths on SFTP.
    """

    def __init__(self, sftp, pattern, root_dir):
        """
        :param hostname:
            Server to connect to, required.
        """
        self.sftp_params = sftp
        self.pattern = pattern
        self.root_dir = root_dir

    def run(self):
        filename_re = re.compile(self.pattern)
        with sftp_connect(**self.sftp_params) as sftp:
            sftp.chdir(self.root_dir)
            for filename in sftp.listdir():
                path = os.path.join(self.root_dir, filename)
                match = filename_re.match(filename)
                if match:
                    yield (path, match)


@contextmanager
def sftp_connect(host, port, username, password):
    transport = paramiko.Transport((host, port))
    try:
        transport.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(transport)
        yield sftp
    finally:
        sftp.close()
        transport.close()

def sftp_walk(sftp, base_path, pattern):
    try:
        files = sftp.listdir_attr(base_path)
    except Exception:
        return []

    matched = []
    for file in files:
        path = f'{base_path}/{file.filename}'

        if S_ISDIR(file.st_mode):
            matched.extend(sftp_walk(sftp, path, pattern))

        if fnmatch.fnmatch(file.filename, pattern):
            matched.append(path)

    return matched

def S_ISDIR(mode):
    """
    Check if mode of file is directory.
    S_ISDIR
    """
    return (mode & 0o170000) == 0o040000

def run(args, cp):
    """
    Select unprocessed files from a source and send them to a queue.
    """
    pass

def config_from_args(args):
    """
    Return config parser from command line arguments.
    """
    cp = configparser.ConfigParser()

    if args.config:
        # Read from command line arguments.
        cp.read(args.config)
    elif CONFIG_VAR in os.environ:
        # Read optional environment variable.
        cp.read(os.environ[CONFIG_VAR])
    else:
        raise ValueError('Unable to find configuration files.')

    return cp

def human_split(string):
    return string.replace(',', ' ').split()

def safer_eval(expr, context):
    return eval(expr, {'__builtins__': {}}, context)

def instance_from_section(section, context):
    class_ = safer_eval(section['class'], context)
    args = safer_eval(section.get('args', '()'), context)
    kwargs = safer_eval(section.get('kwargs', '{}'), context)
    instance = class_(*args, **kwargs)
    return instance

def named_instances(cp, appkey, prefix, context):
    return {
        suffix: instance_from_section(cp[prefix + suffix], context)
        for suffix in human_split(cp[APP][appkey])
    }

def main(argv=None):
    parser = argparse.ArgumentParser(
        description = run.__doc__,
    )
    parser.add_argument(
        '--config',
        action = 'append',
        default = [],
        help =
            'Configuration files. Environment variable'
            f' {CONFIG_VAR} is also loaded.',
    )
    args = parser.parse_args(argv)

    cp = config_from_args(args)

    context = globals().copy()
    context['str'] = str
    context['int'] = int

    patterns = named_instances(cp, 'patterns', 'pattern.', context)
    context['patterns'] = patterns

    schemas = named_instances(cp, 'schemas', 'schema.', context)
    context['schemas'] = schemas

    sources = named_instances(cp, 'sources', 'source.', context)

    for source_name, source in sources.items():
        for path, data in source.run():
            print(path)
            print(data)

if __name__ == '__main__':
    main()
