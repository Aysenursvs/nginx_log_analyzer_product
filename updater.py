def update_ip_record(parsed_line, ip_data):
    """
    Updates the IP data record with the parsed log line information.
    
    :param parsed_line: A dictionary containing parsed log line information
    :param ip_data: A dictionary containing existing IP data records
    """
    ip = parsed_line.get("ip")
    if ip not in ip_data:
        ip_data[ip] = {
            "request_times": [parsed_line.get("datetime")],
            "user_agents": {parsed_line.get("user_agent")},
            "request_count": 1,
            "status_codes": {parsed_line.get("status"): 1},
            "is_bot": False,
            "last_seen": parsed_line.get("datetime")
        }
    else:
        ip_data[ip]["request_times"].append(parsed_line.get("datetime"))
        ip_data[ip]["user_agents"].add(parsed_line.get("user_agent"))
        ip_data[ip]["request_count"] += 1
        ip_data[ip]["status_codes"][parsed_line.get("status")] = ip_data[ip]["status_codes"].get(parsed_line.get("status"), 0) + 1
        ip_data[ip]["last_seen"] = parsed_line.get("datetime")
        