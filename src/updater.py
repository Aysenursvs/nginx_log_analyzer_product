import logging
from analyzer import is_bot_by_user_agent, check_request_count, is_rate_limit_exceeded, calculate_risk_score
from variables import block_risk_score, review_risk_score, request_count_threshold,  rate_limit_window_sec, max_requests, API_KEY
import requests
import time
           
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
        status = parsed_line.get("status") or "unknown"
        ip_datas[ip]["status_codes"][status] = ip_datas[ip]["status_codes"].get(status, 0) + 1
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
    IPINFO_API_KEY = API_KEY
    url = f"https://ipinfo.io/{ip}/json"
    headers = {"Authorization": f"Bearer {IPINFO_API_KEY}"} if IPINFO_API_KEY else {}

    # Check if the prefix is already in the cache
    # If it is, return the cached data if it contains country and city information.
    if prefix in cache and cache[prefix].get("country") and cache[prefix].get("city"):
        if ip not in cache[prefix]["IP"]:
            cache[prefix]["IP"].append(ip)
        return cache[prefix]

    retries = 3
    for attempt in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=3)
            if response.status_code == 200:
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
            else:
                logging.warning(f"IPinfo returned status {response.status_code} for IP {ip}")
        except requests.RequestException as e:
            logging.error(f"[IPinfo Error] Attempt {attempt+1}/{retries} for IP {ip}: {e}")

        time.sleep(0.5)  # Wait for a short period before retrying

    # If all attempts fail, return a default value
    return {"city": None, "country": None, "latlng": None, "IP": [ip]}

# This function extracts the prefix from an IP address.
# It takes an IP address and the number of parts to consider for the prefix.
# The default is to consider the first two parts of the IP address.
# It returns the prefix as a string.
def get_prefix(ip, parts=2):
    if not ip or '.' not in ip:
        return "unknown"
    return '.'.join(ip.split('.')[:parts])


    

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

