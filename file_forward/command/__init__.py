from . import initialize
from . import lcb_message
from . import load
from . import process

def add_parsers(argument_parser):
    for obj in globals().values():
        if hasattr(obj, 'add_parser'):
            obj.add_parser(argument_parser)
