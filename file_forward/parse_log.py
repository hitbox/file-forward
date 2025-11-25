import ast
import logging

from datetime import datetime
from zoneinfo import ZoneInfo

DTFMT = '%Y-%m-%d %H:%M:%S,%f'

def parse_log_tail(tail):
    parts = tail.split(':')
    result = {}

    i = 0
    while i < len(parts):
        if parts[i].startswith('fields='):
            # Capture the whole remaining tail for fields=
            kv = ':'.join(parts[i:])
            key, val = kv.split('=', 1)
            try:
                result[key] = ast.literal_eval(val)
            except Exception:
                result[key] = val
            break
        elif '=' in parts[i]:
            key, val = parts[i].split('=', 1)
            result[key] = val
        elif i + 1 < len(parts):
            # Assume key and value are split across parts
            key = parts[i]
            val = parts[i + 1]
            result[key] = val
            i += 1
        i += 1

    return result

def parse_for_logging(line):
    """
    Parse a line of text as usual logging for datetime, level name and number,
    logger name, and remaining text.
    """
    logging_datetime = datetime.strptime(line[:23], DTFMT)

    # Find the logging level string.
    end_level = line.find(':', 25)
    level_name = line[24:end_level]
    level_integer = getattr(logging, level_name)

    end_logger = line.find(':', end_level+1)
    logger_name = line[end_level+1:end_logger]

    end_message = line.find(':', end_logger+1)
    message = line[end_logger+1:end_message]

    #remaining = ast.literal_eval(line[end_message+1:])
    remaining = line[end_message+1:]

    data = {
        'datetime': logging_datetime,
        'level_name': level_name,
        'level_integer': level_integer,
        'logger_name': logger_name,
        'message': message,
        'data': remaining,
    }
    return data

def parse_log_line(line, timezone=None):
    if timezone is None:
        timezone = 'America/New_York'
    tzinfo = ZoneInfo(timezone)

    logging_datetime = datetime.strptime(line[:23], DTFMT).replace(tzinfo=tzinfo)

    # Find the logging level string.
    end_logging_level = line.find(':', 25)
    logging_level_name = line[24:end_logging_level]
    logging_level_integer = getattr(logging, logging_level_name)

    end_logger_name = line.find(':', end_logging_level+1)
    logger_name = line[end_logging_level+1:end_logger_name]

    end_message = line.find(':', end_logger_name+1)
    message = line[end_logger_name+1:end_message]

    if message == 'message committed':
        # This line is a log line with data.
        log_data = {
            'logging_datetime': logging_datetime,
            'logging_level_name': logging_level_name,
            'logging_level_integer': logging_level_integer,
            'logger_name': logger_name,
        }
        tail = line[end_message+1:]
        tail_data = parse_log_tail(tail)
        log_data.update(tail_data)
        return log_data

def parse_lines(lines):
    data = {}
    for line in lines:
        try:
            line_data = parse_for_logging(line)
        except ValueError:
            # ignore datetime conversion errors.
            pass
        else:
            message = line_data['logger']['message']
            data[message] = line_data
            if message == 'scrape':
                yield data
