def update_ip_record(parsed_line, ip_datas):
    """
    Updates the IP data record with the parsed log line information.
    
    :param parsed_line: A dictionary containing parsed log line information
    :param ip_data: A dictionary containing existing IP data records
    """
    ip = parsed_line.get("ip")
    if ip not in ip_datas:
        ip_datas[ip] = {
            "request_times": [parsed_line.get("datetime")],
            "user_agents": {parsed_line.get("user_agent")},
            "request_count": 1,
            "status_codes": {parsed_line.get("status"): 1},
            "is_bot": False,
            "is_suspicious": False,
            "last_seen": parsed_line.get("datetime"),
            "risk_score": 0,
            "action": "normal"
        }
    else:
        ip_datas[ip]["request_times"].append(parsed_line.get("datetime"))
        ip_datas[ip]["user_agents"].add(parsed_line.get("user_agent"))
        ip_datas[ip]["request_count"] += 1
        ip_datas[ip]["status_codes"][parsed_line.get("status")] = ip_datas[ip]["status_codes"].get(parsed_line.get("status"), 0) + 1
        ip_datas[ip]["last_seen"] = parsed_line.get("datetime")

    return ip_datas[ip]

def update_bot_status(ip_data, bot_status):
    if not ip_data["is_bot"] and bot_status:
        ip_data["risk_score"] += 50
    ip_data["is_bot"] = bot_status
    ip_data["is_suspicious"] = bot_status
    

def update_suspicious_status(ip_data, suspicious_status):
    if not ip_data["is_bot"]:
        if not ip_data["is_suspicious"] and suspicious_status:
            ip_data["risk_score"] += 20
        ip_data["is_suspicious"] = suspicious_status


def update_action_by_risk_score(ip_data: dict) -> str:
    if ip_data["risk_score"] >= 70:
        ip_data["action"] = "block"
    elif ip_data["risk_score"] >= 40:
        ip_data["action"] = "review"
    else:
        ip_data["action"] = "normal"






def print_record(ip_datas):
    for ip, data in ip_datas.items():
        print(f"IP: {ip}")
        print(f"  Request Times: {data['request_times']}")
        print(f"  User Agents: {data['user_agents']}")
        print(f"  Request Count: {data['request_count']}")
        print(f"  Status Codes: {data['status_codes']}")
        print(f"  Is Bot: {data['is_bot']}")
        print(f"  Is Suspicious: {data['is_suspicious']}")
        print(f"  Last Seen: {data['last_seen']}\n")
        print(f"  Risk Score: {data['risk_score']}")
        print(f"  Action: {data['action']}")
        
        
        print("-" * 40)
        print()