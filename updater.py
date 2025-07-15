from anlayzer import is_bot_by_user_agent, check_request_count, is_rate_limit_exceeded, calculate_risk_score
from variables import bot_risk_score, suspicious_risk_score, rate_limit_risk_score, block_risk_score, review_risk_score, request_count_threshold,  rate_limit_window_sec, max_requests
from datetime import datetime
import geocoder
           

def update_ip_record(parsed_line, ip_datas):
    """
    Updates the IP data record with the parsed log line information.
    
    :param parsed_line: A dictionary containing parsed log line information
    :param ip_data: A dictionary containing existing IP data records
    """
    ip = parsed_line.get("ip")
    if ip not in ip_datas:
        ip_datas[ip] = {
            "request_times": [parsed_line.get("datetime_obj")],
            "user_agents": {parsed_line.get("user_agent")},
            "request_count": 1,
            "status_codes": {parsed_line.get("status"): 1},
            "is_bot": False,
            "is_suspicious": False,
            "is_limit_exceeded": False,
            "last_seen": parsed_line.get("datetime_obj"),
            #"country": get_geolocation(ip).get("country"),
            #"city": get_geolocation(ip).get("city"),
            "risk_components": {
                "bot": 0,
                "suspicious": 0,
                "rate_limit": 0
            },

            "risk_score": 0,
            "action": "normal"
        }
    else:
        ip_datas[ip]["request_times"].append(parsed_line.get("datetime_obj"))
        ip_datas[ip]["user_agents"].add(parsed_line.get("user_agent"))
        ip_datas[ip]["request_count"] += 1
        ip_datas[ip]["status_codes"][parsed_line.get("status")] = ip_datas[ip]["status_codes"].get(parsed_line.get("status"), 0) + 1
        ip_datas[ip]["last_seen"] = parsed_line.get("datetime_obj")

    return ip_datas[ip]

def get_geolocation(ip):
    g = geocoder.ip(ip)
    return {
        "city": g.city,
        "country": g.country,
        "latlng": g.latlng
    }

def update_bot_status(ip_data, bot_status):
    if not ip_data["is_bot"] and bot_status:
        ip_data["is_bot"] = bot_status
        
        
    

def update_suspicious_status(ip_data, suspicious_status):
    if not ip_data["is_suspicious"] and suspicious_status:
        ip_data["is_suspicious"] = suspicious_status
        

def update_rate_limit_status(ip_data, rate_limit_status):
    if not ip_data["is_limit_exceeded"] and rate_limit_status:
        ip_data["is_limit_exceeded"] = rate_limit_status
        

def update_action_by_risk_score(ip_data: dict) -> str:
    if ip_data["risk_score"] >= block_risk_score:
        ip_data["action"] = "block"
    elif ip_data["risk_score"] >= review_risk_score:
        ip_data["action"] = "review"
    else:
        ip_data["action"] = "normal"





def update_ip_status(ip_data):
    bot_status = is_bot_by_user_agent(ip_data["user_agents"])
    update_bot_status(ip_data, bot_status)
    suspicious_status = check_request_count(ip_data, request_count_threshold)
    update_suspicious_status(ip_data, suspicious_status)
    rate_limit_status = is_rate_limit_exceeded(ip_data,  rate_limit_window_sec, max_requests)
    update_rate_limit_status(ip_data, rate_limit_status)
    calculate_risk_score(ip_data)
    
    update_action_by_risk_score(ip_data)


def print_record(ip_datas):
    for ip, data in ip_datas.items():
        print(f"IP: {ip}")
        print(f"  Request Times: {data['request_times']}")
        print(f"  User Agents: {data['user_agents']}")
        print(f"  Request Count: {data['request_count']}")
        print(f"  Status Codes: {data['status_codes']}")
        print(f"  Is Bot: {data['is_bot']}")
        print(f"  Is Suspicious: {data['is_suspicious']}")
        print(f"  Is Rate Limit Exceeded: {data['is_limit_exceeded']}")
        print(f"  Last Seen: {data['last_seen']}\n")
        #print(f"  Country: {data['country']}")
        #print(f"  City: {data['city']}")
        print(f"  Risk Components:")
        print(f"    Bot: {data['risk_components']['bot']}")
        print(f"    Suspicious: {data['risk_components']['suspicious']}")
        print(f"    Rate Limit: {data['risk_components']['rate_limit']}")
        print(f"  Risk Score: {data['risk_score']}")
        print(f"  Action: {data['action']}")
        
        
        print("-" * 40)
        print()