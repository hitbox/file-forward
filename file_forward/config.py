import configparser
import os
import re

from file_forward import core
from file_forward.util import human_split

APP = 'file_forward'
CONFIG_VAR = 'FILE_FORWARD_CONFIG'

class InstantiateConfig:

    def __init__(self, named_items):
        """
        :param named_items:
            List of pairs (key, prefix). The key is to a name in the app config
            section and prefix is the prefix to find another section from the
            values in the app config.
        """
        self.named_items = named_items

    def __call__(self, cp):
        context = {}
        context['str'] = str
        context['int'] = int
        context['re'] = re
        context.update(core._context())

        result = {}
        for key, prefix in self.named_items:
            instances = named_instances(cp, key, prefix, context)
            result[key] = instances
            context[key] = instances
        return result


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

def safer_eval(expr, context):
    return eval(expr, {'__builtins__': {}}, context)

def instance_from_section(section, context):
    """
    Instantiate from config section.
    """
    class_ = safer_eval(section['class'], context)
    args = safer_eval(section.get('args', '()'), context)
    kwargs = safer_eval(section.get('kwargs', '{}'), context)
    instance = class_(*args, **kwargs)
    return instance

def named_instances(cp, appkey, prefix, context):
    """
    Split a key's value and find sections to instance from, creating a dict of
    named instances.
    """
    return {
        suffix: instance_from_section(cp[prefix + suffix], context)
        for suffix in human_split(cp[APP][appkey])
    }
