from analyzer import is_bot_by_user_agent, check_request_count, is_rate_limit_exceeded, calculate_risk_score
from variables import block_risk_score, review_risk_score, request_count_threshold,  rate_limit_window_sec, max_requests
from datetime import datetime
import requests
           
# This function updates the IP record with the parsed log line.
# It extracts the IP address, prefix, and other relevant information from the parsed line.
# It updates the IP data in the ip_datas dictionary and increments the prefix counter.
# It returns the updated IP data.
# It is used in the main.py file to update the IP data after parsing each log line
def update_ip_record(parsed_line, ip_datas, cache, prefix_counter):
    ip = parsed_line.get("ip")

    prefix = get_prefix(ip, parts=2)
    prefix_counter[prefix] = prefix_counter.get(prefix, 0) + 1

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
            "country": get_geolocation_by_request(ip, cache, prefix).get("country"),
            "city": get_geolocation_by_request(ip, cache, prefix).get("city"),
            "prefix": prefix,
            "risk_components": {    # Risk components for risk score calculation
                "bot": 0,           # Determined by checking user agents
                "suspicious": 0,    # Determined by checking is_suspicious flag
                "rate_limit": 0,    # Determined by checking is_limit_exceeded flag
                "prefix": 0,        # Determined by checking prefix request count
                "location": 0       # Determined by checking geolocation data
            },

            "risk_score": 0,
            "action": "normal",
            "review_warning": False,
            "block_warning": False
        }
    else:
        ip_datas[ip]["request_times"].append(parsed_line.get("datetime_obj"))
        ip_datas[ip]["user_agents"].add(parsed_line.get("user_agent"))
        ip_datas[ip]["request_count"] += 1
        ip_datas[ip]["status_codes"][parsed_line.get("status")] = ip_datas[ip]["status_codes"].get(parsed_line.get("status"), 0) + 1
        ip_datas[ip]["last_seen"] = parsed_line.get("datetime_obj")

    return ip_datas[ip]


# This function retrieves the geolocation information for a given IP address.
# It uses the IPinfo API to get the city and country information.
# If the IP address is already in the cache, it returns the cached data.
# If the IP address is not in the cache, it makes a request to the IPinfo API to get the geolocation data.
# It returns a dictionary containing the city, country, latitude, longitude, and a list of IPs associated with that prefix.
# It is used in the update_ip_record function to get the geolocation information for the IP address.
# The cache is a dictionary where the keys are prefixes and the values are dictionaries containing the geolocation data.
# The prefix is determined by the first two octets of the IP address.
def get_geolocation_by_request(ip, cache, prefix):
    IPINFO_API_KEY = "1110fe2e554f9d"
    
    if prefix in cache and cache[prefix].get("country") and cache[prefix].get("city"):
        if ip not in cache[prefix]["IP"]:
            cache[prefix]["IP"].append(ip)
        return cache[prefix]
    
    try:
        url = f"https://ipinfo.io/{ip}/json"
        headers = {"Authorization": f"Bearer {IPINFO_API_KEY}"} if IPINFO_API_KEY else {}
        response = requests.get(url, headers=headers, timeout=3)
        data = response.json()

        city = data.get("city")
        country = data.get("country")
        loc = data.get("loc")  # "latitude,longitude"
        latlng = list(map(float, loc.split(","))) if loc else None

        location = {
            "city": city,
            "country": country,
            "latlng": latlng,
            "IP": [ip],
        }
        cache[prefix] = location
        return location
    except Exception as e:
        print(f"[IPinfo Error] {e}")
        return {"city": None, "country": None, "latlng": None, "IP": [ip]}

# This function extracts the prefix from an IP address.
# It takes an IP address and the number of parts to consider for the prefix.
# The default is to consider the first two parts of the IP address.
# It returns the prefix as a string.
def get_prefix(ip, parts=2):
    return '.'.join(ip.split('.')[:parts])

# This function saves a warning messages to a dictionary.
# It takes a warnings dictionary, a warning message, an IP address, and an optional line number.
# If the IP address is not already in the warnings dictionary, it initializes a new entry
# with an empty list for messages and line numbers.
# It appends the warning message to the list of messages and the line number to the list
# of line numbers for that IP address.
# This function is used to keep track of warnings for each IP address.
def update_warning(warnings_dict, warning_message, ip, line_number=None):
    if ip not in warnings_dict:
        warnings_dict[ip] = {"messages": [], "line_numbers": []}
    
    warnings_dict[ip]["messages"].append(warning_message)
    if line_number is not None:
        warnings_dict[ip]["line_numbers"].append(line_number)
    

# ******************************************************
# GENERAL UPDATE FUNCTIONS PART
# ******************************************************

# This function updates the bot status in the IP data.
# It checks the is_bot flag in the IP data and updates it based on the bot status.
# If the IP is not already marked as a bot and the bot status is True, it updates the is_bot flag to True.
def update_bot_status(ip_data, bot_status):
    if not ip_data["is_bot"] and bot_status:
        ip_data["is_bot"] = bot_status
        
        
# This function updates the suspicious status in the IP data.
# It checks the is_suspicious flag in the IP data and updates it based on the suspicious status.
# If the IP is not already marked as suspicious and the suspicious status is True,
# it updates the is_suspicious flag to True.    
def update_suspicious_status(ip_data, suspicious_status):
    if not ip_data["is_suspicious"] and suspicious_status:
        ip_data["is_suspicious"] = suspicious_status
        
#This function updates the rate limit status in the IP data.
# It checks the is_limit_exceeded flag in the IP data and updates it based on the rate limit status.
# If the IP is not already marked as rate limit exceeded and the rate limit status is True,
# it updates the is_limit_exceeded flag to True.
def update_rate_limit_status(ip_data, rate_limit_status):
    if not ip_data["is_limit_exceeded"] and rate_limit_status:
        ip_data["is_limit_exceeded"] = rate_limit_status
        
# This function updates the action based on the risk score and the defined thresholds.
# It sets the action to "block" if the risk score is greater than or equal to the block risk score,
# to "review" if the risk score is greater than or equal to the review risk score,
# and to "normal" otherwise.
def update_action_by_risk_score(ip_data: dict) -> str:
    if ip_data["risk_score"] >= block_risk_score:
        ip_data["action"] = "block"
    elif ip_data["risk_score"] >= review_risk_score:
        ip_data["action"] = "review"
    else:
        ip_data["action"] = "normal"


# This function make all updates to the IP data.
# It checks the bot status, suspicious status, and rate limit status,
# updates the IP data accordingly, and calculates the risk score.
# It also updates the action based on the risk score.
# It is called in the main.py file after parsing each log line.
def update_ip_status(ip_data, prefix_counter=None):

    bot_status = is_bot_by_user_agent(ip_data["user_agents"])
    update_bot_status(ip_data, bot_status) 

    suspicious_status = check_request_count(ip_data, request_count_threshold)
    update_suspicious_status(ip_data, suspicious_status)

    rate_limit_status = is_rate_limit_exceeded(ip_data,  rate_limit_window_sec, max_requests)
    update_rate_limit_status(ip_data, rate_limit_status)

    calculate_risk_score(ip_data, prefix_counter)

    update_action_by_risk_score(ip_data)

# This function prints the IP data in a readable format.
# It iterates through the IP data dictionary and prints the relevant information for each IP.
# It is used for debugging purposes to see the IP data after processing.
# It can be called in the main.py file to print the IP data after processing all log lines.
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
        print(f"  Country: {data['country']}")
        print(f"  City: {data['city']}")
        print(f"  Risk Components:")
        print(f"    Bot: {data['risk_components']['bot']}")
        print(f"    Suspicious: {data['risk_components']['suspicious']}")
        print(f"    Rate Limit: {data['risk_components']['rate_limit']}")
        print(f"    Prefix: {data['risk_components']['prefix']}")
        print(f"    Location: {data['risk_components']['location']}")
        print(f"  Risk Score: {data['risk_score']}")
        print(f"  Action: {data['action']}")
        
        
        print("-" * 40)
        print()