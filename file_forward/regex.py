import re

regexes = {
    # OptiClimb PDF files.
    'opticlimb_filename_regex': re.compile(
        # Matching and capturing like these:
        # 'OptiFlight-ABX3107-16APR25-KSCK-OFP4.pdf'
        # 'OptiFlight-ATN3335-16APR25-KONT-OFP14_0_1.pdf'
        # 'OptiFlight-ATN3335-16APR25-KONT-OFP13_0_1.pdf'
        r'OptiFlight-(?P<airline_icao>[A-Z]{3})'
        r'(?P<flight_number>[A-Z0-9]{2}\d{1,4}[A-Z]?)'
        r'-(?P<flight_date_string>\d{2}[a-zA-Z]{3}\d{2})'
        r'-(?P<departure_icao>[A-Z]{4})'
        r'-OFP(?P<ofp_string>[\d_]+)'
        r'.pdf',
    ),
    # ASM Text files
    'asm_regex': re.compile(
        # ASM_ABX_819_2_31MAY25_0115_0230_SFO_LAX.txt
        r'ASM_(?P<airline_icao>[A-Z]{3})'
        r'_(?P<flight_number>[0-9]{1,4})'
        r'_(?P<number1>\d+)'
        r'_(?P<flight_date_string>\d{2}[a-zA-Z]{3}\d{2})'
        r'_(?P<time1>\d{4})'
        r'_(?P<time2>\d{4})'
        r'_(?P<origin_iata>[A-Z]{3})'
        r'_(?P<destination_iata>[A-Z]{3})'
        r'.txt'
    ),
}

# Convenience
opticlimb_filename_regex = regexes['opticlimb_filename_regex']
asm_regex = regexes['asm_regex']
