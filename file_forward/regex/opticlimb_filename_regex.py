import re

# OptiClimb PDF file names.

opticlimb_filename_regex = re.compile(
    # Matching and capturing like these:
    # 'OptiFlight-ABX3107-16APR25-KSCK-OFP4.pdf'
    # 'OptiFlight-ATN3335-16APR25-KONT-OFP14_0_1.pdf'
    # 'OptiFlight-ATN3335-16APR25-KONT-OFP13_0_1.pdf'
    r'OptiFlight-(?P<airline_icao>[A-Z]{3})'
    r'(?P<flight_number>[A-Z0-9]{2}\d{1,4}[A-Z]?)'
    r'-(?P<flight_date_string>\d{2}[a-zA-Z]{3}\d{2})'
    r'-(?P<departure_icao>[A-Z]{4})'
    r'-OFP(?P<ofp_version>[\d_]+)'
    r'.pdf'
)
