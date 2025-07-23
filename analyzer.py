from datetime import datetime, timedelta

# ********************************************************
# ANALYZE AND UPDATE IP DATA RELATED FLAGS PART
# ********************************************************

# This function checks if the user agent is a bot based on known phrases.
# It returns True if any of the phrases are found in the user agent string.
def is_bot_by_user_agent(user_agents: list[str]) -> bool:
    known_bots_pharases = ["bot", "crawl", "spider", "slurp", "archive", "checker"]

    for user_agent in user_agents:
        lower_user_agent = user_agent.lower()
        for phrase in known_bots_pharases:
            if phrase in lower_user_agent:
                return True
    return False

# This function checks if the request count exceeds a given threshold.
# It returns True if the request count is greater than the threshold.
# The threshold is set to 10000 by default.
def check_request_count(ip_data: dict, threshold: int = 10000) -> bool:
    return ip_data.get("request_count", 0) > threshold

# This function checks if the rate limit is exceeded based on the number of requests in the last `window_sec` seconds.
# It returns True if the number of requests in the last `window_sec` seconds is greater than or equal to `max_requests`.
# The default values for `window_sec` and `max_requests` are 60 and 100, respectively.
def is_rate_limit_exceeded(ip_data: dict, window_sec: int = 60, max_requests: int = 100) -> bool:
    now = datetime.now()
    recent_requests = [t for t in ip_data["request_times"] if now - t <= timedelta(seconds=window_sec)]
    return len(recent_requests) >= max_requests

# ****************************************************************
# ANALYZE AND CALCULATE RISK SCORES PART
# ***************************************************************

# This function checks if the user agent is unknown or weird.
# It returns True if the user agent is empty, too short, does not contain any letters,
# or contains only non-alphabetic characters.
def is_unknown_or_weird_user_agent(ua: str) -> bool:
    ua = ua.strip()
    if ua == "" or ua == "-":
        return True
    if len(ua) < 10:
        return True
    if not any(c.isalpha() for c in ua):  # hiç harf içermiyorsa
        return True
    return False

# This function calculates the bot risk score based on the user agents.
# It returns a risk score based on the presence of known safe bots, suspicious agents,
# unknown bots, weird user agents, and the number of unique user agents.
# It returns a risk score based on the analysis.
# You can change the risk scores for known safe bots, suspicious agents, unknown bots, weird user agents, and the number of unique user agents.
# You can update the known safe bots list, suspicious agents list.
def calculate_bot_risk(ip_data):
    known_safe_bots = ["google", "bing", "yandex", "baiduspider", "facebook"]
    suspicious_agents = ["python", "curl", "wget", "requests", "scrapy", "aiohttp"]

    user_agents = ip_data.get("user_agents", [])
    risk = 0
    has_tool = False
    has_unknown_bot = False
    has_safe_bot = False
    has_weird_ua = False

    for ua in user_agents:
        ua_lower = ua.lower()

        if any(bot in ua_lower for bot in known_safe_bots):
            has_safe_bot = True
        elif any(tool in ua_lower for tool in suspicious_agents):
            has_tool = True
        elif "bot" in ua_lower or "spider" in ua_lower or "crawl" in ua_lower:
            has_unknown_bot = True
        elif is_unknown_or_weird_user_agent(ua_lower):
            has_weird_ua = True

    if has_tool:
        risk += 30 # If a tool is detected, it indicates suspicious/bot behavior.
    if has_unknown_bot:
        risk += 20 # If an unknown bot is detected, it indicates suspicious behavior.
    if has_safe_bot:
        risk += 5 # If a safe bot is detected, it indicates usual bot behavior. Ex: Googlebot
    if has_weird_ua:
        risk += 15 # If a weird user agent is detected, it indicates suspicious behavior. Ex: empty, too short, no letters, etc.
    if len(user_agents) > 10:
        risk += 5 # If there are more than 10 unique user agents, it indicates suspicious behavior.

    return risk

# This function calculates the suspicious risk score based on the suspicious flag.
# It returns a risk score of 30 if the suspicious flag is True, otherwise it returns 0.
# The suspicious flag indicates if the IP is suspicious based on the request count.
# You can change the risk score for suspicious IPs here.
# The default value is 30.    
def calculate_suspicious_risk_by_suspicious_flag(ip_data) -> int:
    if ip_data.get("is_suspicious", False):
        return 15
    return 0

# This function calculates the rate limit risk score based on the rate limit exceeded flag.
# It returns a risk score of 30 if the rate limit is exceeded, otherwise it returns 0.
# The rate limit exceeded flag indicates if the IP has exceeded the rate limit based on the number of requests in the last `window_sec` seconds.
# You can change the risk score for rate limit exceeded IPs here.
# The default value is 30.
def calculate_rate_limit_risk(ip_data) -> int:
    if ip_data["is_limit_exceeded"]:
        return 25
    return 0

# This function calculates the prefix risk score based on the prefix counter.
# It returns a risk score of 10 if the prefix count is greater than the threshold and the request count is not equal to the prefix count.
# If request count is equal to prefix count, it means there is one IP address that have this prefix. 
# This is not suspicious.
# The prefix threshold is set to 500 by default.
# The high risk score is set to 10 by default.
# You can change the prefix threshold and the risk score here.
def calculate_prefix_risk(ip_data, prefix_counter, prefix_threshold=300, high_risk_score=10):
    prefix_count = prefix_counter.get(ip_data.get("prefix"), None)
    if ip_data.get("request_count") != prefix_count and prefix_count  > prefix_threshold:
        return high_risk_score
    return 0

# This function calculates the location risk score based on the country.
# It returns a risk score of 20 if the country is suspicious, otherwise it returns 0.
# The suspicious countries are defined in the function.
# If the country is not found, it returns a risk score of 20.
# You can change the suspicious countries and the risk score here.
# The default value is 20.
def calculate_location_risk(ip_data):
    country = ip_data.get("country")
    suspicious_flag = ip_data.get("is_suspicious", False)

    # Suspicious flag True değilse, lokasyona göre risk ekleme
    if not suspicious_flag:
        return 0

    # Lokasyon verisi yoksa (geolocation başarısız)
    if country is None or country.strip() == "":
        return 15

    # Şüpheli ülkeler listesi
    suspicious_countries = ["RU", "CN", "KP", "IR", "NG", "BR", "VN"]

    if country in suspicious_countries:
        return 20
    else:
        return 0


# This function calculates the total risk score based on various risk components by calling the individual risk calculation functions.
# It updates the risk components in the IP data and returns the total risk score.
# The risk components are: bot, suspicious, rate limit, prefix, and location.
def calculate_risk_score(ip_data, prefix_counter= None):
    bot_risk = calculate_bot_risk(ip_data)
    suspicious_risk = calculate_suspicious_risk_by_suspicious_flag(ip_data)
    rate_limit_risk = calculate_rate_limit_risk(ip_data)
    location_risk = calculate_location_risk(ip_data)
    prefix_risk = 0

    if prefix_counter is not None:
        prefix_risk = calculate_prefix_risk(ip_data, prefix_counter)

    ip_data["risk_components"]["bot"] = bot_risk
    ip_data["risk_components"]["suspicious"] = suspicious_risk
    ip_data["risk_components"]["rate_limit"] = rate_limit_risk
    ip_data["risk_components"]["prefix"] = prefix_risk
    ip_data["risk_components"]["location"] = location_risk

    ip_data["risk_score"] = bot_risk + suspicious_risk + rate_limit_risk + prefix_risk + location_risk

# ********************************************************