
def parse_log_line(line):
    """
    Parses a single line of the log file and extracts relevant information.
    
    :param line: A line from the log file
    :return: A dictionary containing the parsed information
    """
    # Example: 127.0.0.1 - - [01/Jan/2020:00:00:01 +0000] "GET /index.html HTTP/1.1" 200 1234
    try:
        ip, _, _, datetime, request, status, size, referer, user_agent = line.split(" ", 8)
        return {
            "ip": ip,
            "datetime": datetime,
            "request": request,
            "status": status,
            "size": size,
            "referer": referer,
            "user_agent": user_agent
        }
    except ValueError:
        return None
