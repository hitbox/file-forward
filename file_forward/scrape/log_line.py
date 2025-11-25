import re

"""
2025-08-06 13:19:19,845:DEBUG:file_forward.output.lcb_output:message committed:{'host': 'ATSGLIDOMQ01', 'queue': 'ABX.ATSGLIDOLEG01.RCV.LCB_ABD', 'fields': {'JMSType': 'Byte', 'JMSExpiration': None, 'LidoMeta': '{"legIdentifier": "GB.3130.06Aug25.AFW.RFD.", "documents": [{"docKey": "LCB", "fileName": "OptiFlight-ABX3130-06AUG25-KAFW-OFP5.pdf", "mediaType": "application/pdf"}]}'}}
"""

message_committed_re = re.compile(
    r'(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})'
    r':(?P<level_name>DEBUG)'
    r':(?P<logger_name>file_forward.output.lcb_output)'
    r':(?P<message>message committed)'
    r':(?P<data>.*$)'
)


"""
2025-08-06 15:22:17,642:DEBUG:file_forward.scan.scan:scrape:{'airline_icao': 'ABX', 'flight_number': '3130', 'flight_date_string': '06AUG25', 'departure_icao': 'KAFW', 'ofp_version': '7', 'aircraft_registration': 'N1489A', 'destination_icao': 'KRFD', 'take_off_weight_pounds': '265440', 'block_off_time': '20:00', 'block_in_time': '22:07'}
"""


scan_and_scrape_re = re.compile(
    r'(?P<datetime>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})'
    r':(?P<level_name>DEBUG)'
    r':(?P<logger_name>file_forward.scan.scan)'
    r':(?P<message>scrape)'
    r':(?P<data>.*$)'
)
