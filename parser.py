import re
from datetime import datetime

# This function parses a log line and returns a dictionary with the parsed information.
# It extracts the IP address, datetime, request, status code, size, referer,
# and user agent from the log line.
# The log line format is expected to be:
# <ip> - - [<datetime>] "<request>" <status> <size> "<referer>" "<user_agent>"
# Example: 95.108.213.89 - - [15/Jul/2025:00:05:20 +0300] "GET /bitstream/11147/3469/1/T000581.pdf HTTP/1.1" 200 944600 "-" "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0"

def parse_log_line(line):
    
    try:
        match = re.match(r'(\S+) - - \[([^\]]+)\] "([^"]+)" (\d+) (\d+) "([^"]*)" "([^"]*)"', line)
        if not match:
            return None
        ip = match.group(1)
        datetime_str = match.group(2).split(' ')[0]
        utc = match.group(2).split(' ')[1] if ' ' in match.group(2) else ''
        request = match.group(3)
        status = match.group(4)
        size = match.group(5)
        referer = match.group(6)
        user_agent = match.group(7)

        dt_obj = None
        try:
            dt_obj = datetime.strptime(datetime_str, "%d/%b/%Y:%H:%M:%S %z")  # try with offset, with offset example: 15/Jul/2025:00:05:20 +0300
        except ValueError:
            try:
                dt_obj = datetime.strptime(datetime_str, "%d/%b/%Y:%H:%M:%S")  # try without offset, without offset example: 15/Jul/2025:00:05:20
            except ValueError:
                return None
        
        return {
            "ip": ip,
            "datetime": datetime_str,
            "datetime_obj": dt_obj,
            "utc": utc,
            "request": request,
            "status": status,
            "size": size,
            "referer": referer,
            "user_agent": user_agent
        }
    except ValueError:
        return None
