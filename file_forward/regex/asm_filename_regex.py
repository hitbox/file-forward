import re

# ASM Text file names.

asm_filename_regex = re.compile(
    # ASM_ABX_819_2_31MAY25_0115_0230_SFO_LAX.txt
    r'ASM_(?P<airline_icao>[A-Z]{3})'
    r'_(?P<flight_number>[0-9]{1,4})'
    r'_(?P<number1>\d+)'
    r'_(?P<flight_date_string>\d{2}[a-zA-Z]{3}\d{2})'
    r'_(?P<time1>\d{4})'
    r'_(?P<time2>\d{4})'
    r'_(?P<departure_iata>[A-Z]{3})'
    r'_(?P<destination_iata>[A-Z]{3})'
    r'.txt'
)
