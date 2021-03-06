import pendulum
import re

def parse_time(string):
    match = re.match(r'(\d{4}\d{2}\d{2})(\d{2})?(\d{2})?', string)
    if match.group(3):
        return pendulum.from_format(string, 'YYYYMMDDHHmm')
    if match.group(2):
        return pendulum.from_format(string, 'YYYYMMDDHH')
    else:
        return pendulum.from_format(string, 'YYYYMMDD')

def parse_time_range(string):
    match =re.match(r'(\d{4}\d{2}\d{2}\d{2})-(\d{4}\d{2}\d{2}\d{2})', string)
    if not match:
        raise argparse.ArgumentError('"' + string + '" is not a time range (YYYYMMDDHH-YYYYMMDDHH)!')
    return (pendulum.from_format(match.group(1), 'YYYYMMDDHH'), pendulum.from_format(match.group(2), 'YYYYMMDDHH'))

def parse_forecast_hours(string):
    match = re.match(r'(\d+)-(\d+)\+(\d+)', string)
    if match:
        start = int(match.group(1))
        end   = int(match.group(2))
        step  = int(match.group(3))
        return [x for x in range(start, end + step, step)]
    match = re.findall(r'(\d+):?', string)
    if match:
        return [int(match[i] for i in range(len(match)))]