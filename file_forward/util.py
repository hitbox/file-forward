import operator

from functools import reduce

def bitwise_or(*args):
    return reduce(operator.or_, args)
