import ast
import logging
import re

from collections import defaultdict
from operator import itemgetter
from pprint import pprint

import sqlalchemy as sa

from sqlalchemy.orm import Session

from file_forward import context
from file_forward.configlib import add_config_option
from file_forward.configlib import engine_from_config
from file_forward.model import AircraftRegistration
from file_forward.model import Airline
from file_forward.model import Airport
from file_forward.model import File
from file_forward.model import LCBMessageModel
from file_forward.model import LegIdentifierModel
from file_forward.model import MessageCommitted
from file_forward.model.lido import LegIdentifierField
from file_forward.parse_log import parse_for_logging
from file_forward.parse_log import parse_log_line
from file_forward.schema import MessageCommittedSchema
from file_forward.schema import ScanScrapeSchema
from file_forward.scrape import message_committed_re
from file_forward.scrape import scan_and_scrape_re
from file_forward.util import load_pyfile

logger = logging.getLogger(__name__)

get_leg_identifier = itemgetter(
    'airline_code',
    'date_of_origin',
    'departure_airport',
    'destination_airport',
    'flight_number',
)

def combine_dicts(*dicts):
    result = {}
    for dict_ in dicts:
        result.update(dict_)
    return result

def get_message_committed_leg_identifier(line_data):
    return get_leg_identifier(line_data['data']['fields']['LidoMeta']['legIdentifier'])

def get_flight_data_for_message_committed(line_data):
    flight_data = {
        'airline_iata': line_data['airline_code'],
        'date_of_origin': line_data['date_of_origin'],
        'departure_airport': line_data['departure_airport'],
        'destination_airport': line_data['destination_airport'],
        'flight_number': line_data['flight_data'],
    }
    return flight_data

def update_scrape_for_mappers(line_data, airline_mapper, airport_mapper):
    line_data['data']['airline_code'] = airline_mapper.iata(line_data['data']['airline_icao'])
    line_data['data']['departure_airport'] = airport_mapper.iata(line_data['data']['departure_icao'])
    line_data['data']['destination_airport'] = airport_mapper.iata(line_data['data']['destination_icao'])
    line_data['data']['date_of_origin'] = line_data['data']['flight_date_string']

    del line_data['data']['flight_date_string']

def load_from_logs(args):
    """
    Parse log files and create MessageCommitted objects.
    """
    appconfig = load_pyfile(args.config)
    engine = engine_from_config(appconfig)

    airline_mapper = appconfig.airline_mapper
    airport_mapper = appconfig.airport_mapper

    message_committed_schema = MessageCommittedSchema()
    scan_and_scrape_schema = ScanScrapeSchema()

    re_list = [
        scan_and_scrape_re,
        message_committed_re,
    ]

    keyed_data = defaultdict(list)

    # Load data from log files.
    for fn in args.files:
        with open(fn, 'r') as log_file:
            for line in log_file:
                for regex in re_list:
                    match = regex.match(line)
                    if match:
                        line_data = match.groupdict()
                        try:
                            line_data['data'] = ast.literal_eval(line_data['data'])
                        except SyntaxError:
                            continue
                        message = line_data['message']
                        if message == 'message committed':
                            # This literal_eval should never fail.
                            lido_meta = line_data['data']['fields']['LidoMeta']
                            line_data['data']['fields']['LidoMeta'] = ast.literal_eval(lido_meta)
                            line_data = message_committed_schema.load(line_data)
                            flight_data = line_data['data']['fields']['LidoMeta']['legIdentifier']
                            key = get_message_committed_leg_identifier(line_data)

                        elif message == 'scrape':
                            line_data = scan_and_scrape_schema.load(line_data)
                            update_scrape_for_mappers(line_data, airline_mapper, airport_mapper)
                            key = get_leg_identifier(line_data['data'])
                            flight_data = line_data['data']

                        else:
                            raise ValueError

                        # Update data keyed by leg identifier.
                        keyed_data[key].append(flight_data)

    # Keep only the exactly two pairs matches.
    data_list = [
        combine_dicts(*flight_data_list)
        for key, flight_data_list in keyed_data.items()
        if len(flight_data_list) == 2
    ]

    with Session(engine) as session:
        for flight_data in data_list:
            airline = Airline.one_by_iata(session, flight_data['airline_code'])
            aircraft_registration = AircraftRegistration.get_or_create(session, flight_data['aircraft_registration'])
            departure = Airport.one_by_iata(session, flight_data['departure_airport'])
            destination = Airport.one_by_iata(session, flight_data['destination_airport'])

            flight_number = flight_data['flight_number']
            flight_date = flight_data['date_of_origin']
            operational_suffix = flight_data['operational_suffix']
            take_off_weight = flight_data['take_off_weight_pounds']
            block_in_time = flight_data['block_in_time']
            block_off_time = flight_data['block_off_time']
            ofp_version = flight_data['ofp_version']

            stmt = (
                sa.select(LegIdentifierModel)
                .where(
                    LegIdentifierModel.airline == airline,
                    LegIdentifierModel.flight_number == flight_number,
                    LegIdentifierModel.flight_date == flight_date,
                    LegIdentifierModel.aircraft_registration == aircraft_registration,
                    LegIdentifierModel.departure == departure,
                    LegIdentifierModel.destination == destination,
                )
            )
            leg_identifier = session.scalars(stmt).one_or_none()

            if leg_identifier is None:
                leg_identifier = LegIdentifierModel(
                    airline = airline,
                    flight_number = flight_number,
                    flight_date = flight_date,
                    aircraft_registration = aircraft_registration,
                    departure = departure,
                    destination = destination,
                    operational_suffix = operational_suffix,
                    take_off_weight = take_off_weight,
                    block_in_time = block_in_time,
                    block_off_time = block_off_time,
                    ofp_version = ofp_version,
                )
                session.add(leg_identifier)

        if args.commit:
            session.commit()
