# NOTE:
# During testing, a space was the only value that worked.
# During production testing, empty string worked. It needs the dot separator
# but and empty string.
DEFAULT_OPERATIONAL_SUFFIX = ''

LEG_IDENTIFIER_KEYS = [
    'airline_iata',
    'flight_number',
    'flight_date',
    'departure_iata',
    'destination_iata',
    'operational_suffix',
]

OFP_VERSION_KEYS = [
    'ofp_version_major',
    'ofp_version_minor',
    'ofp_version_patch',
]
