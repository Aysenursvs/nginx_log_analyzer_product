from datetime import datetime, timedelta
from variables import bot_risk_score, suspicious_risk_score, rate_limit_risk_score

def is_bot_by_user_agent(user_agents: list[str]) -> bool:
    known_bots_pharases = ["bot", "crawl", "spider", "slurp", "archive", "checker"]

    for user_agent in user_agents:
        lower_user_agent = user_agent.lower()
        for phrase in known_bots_pharases:
            if phrase in lower_user_agent:
                return True
    return False

def check_request_count(ip_data: dict, threshold: int = 10000) -> bool:
    return ip_data.get("request_count", 0) > threshold

def is_rate_limit_exceeded(ip_data: dict, window_sec: int = 60, max_requests: int = 100) -> bool:
    now = datetime.now()
    recent_requests = [t for t in ip_data["request_times"] if now - t <= timedelta(seconds=window_sec)]
    return len(recent_requests) >= max_requests

# AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
######   Eklenen Risk Skorlar değişiklik gösterebilir ya da bir değişkene atanıp o değişken değerleri kullanılabilir.
def calculate_bot_risk(ip_data):
    known_safe_bots = ["googlebot", "bingbot", "yandexbot", "baiduspider"]
    suspicious_agents = ["python", "curl", "wget", "requests", "scrapy", "aiohttp"]

    user_agents = ip_data.get("user_agents", [])
    risk = 0

    for ua in user_agents:
        ua_lower = ua.lower()

        if any(bot in ua_lower for bot in known_safe_bots):
            risk += 10  # tanınan bot → düşük risk
        elif any(tool in ua_lower for tool in suspicious_agents):
            risk += 40  # tool ile gelen → yüksek risk
        elif "bot" in ua_lower or "spider" in ua_lower or "crawl" in ua_lower:
            risk += 25  # bot ama türü bilinmiyor → orta risk

    return risk


def calculate_suspicious_risk_by_request_count(ip_data) -> int:
    count = ip_data.get("request_count", 0)
    if count < 1000:
        return 0
    elif count < 5000:
        return 10
    elif count < 10000:
        return 20
    else:
        return 40
    
def calculate_suspicious_risk_by_suspicious_flag(ip_data) -> int:
    if ip_data.get("is_suspicious", False):
        return 30
    return 0

def calculate_rate_limit_risk(ip_data) -> int:
    if ip_data["is_limit_exceeded"]:
        return 30
    return 0


def calculate_risk_score(ip_data):
    bot_risk = calculate_bot_risk(ip_data)
    suspicious_risk = calculate_suspicious_risk_by_suspicious_flag(ip_data)
    rate_limit_risk = calculate_rate_limit_risk(ip_data)

    ip_data["risk_components"]["bot"] = bot_risk
    ip_data["risk_components"]["suspicious"] = suspicious_risk
    ip_data["risk_components"]["rate_limit"] = rate_limit_risk

    ip_data["risk_score"] = bot_risk + suspicious_risk + rate_limit_risk



