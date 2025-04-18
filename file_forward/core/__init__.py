from .schema import FlightDate
from .schema import Schema
from .source import PatternSource
from .source import SFTPGlob
from .version import OFPVersion

def _context():
    return {
        'FlightDate': FlightDate,
        'Schema': Schema,
        'PatternSource': PatternSource,
        'SFTPGlob': SFTPGlob,
        'OFPVersion': OFPVersion,
    }
