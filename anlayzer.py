from datetime import datetime, timedelta

def is_bot_by_user_agent(user_agents: list[str]) -> bool:
    known_bots_pharases = ["bot", "crawl", "spider", "slurp", "archive", "checker"]

    for user_agent in user_agents:
        lower_user_agent = user_agent.lower()
        for phrase in known_bots_pharases:
            if phrase in lower_user_agent:
                return True
    return False

def check_request_count(ip_data: dict, threshold: int = 100) -> bool:
    return ip_data.get("request_count", 0) > threshold

def is_rate_limit_exceeded(ip_data: dict, window_sec: int = 60, max_requests: int = 100) -> bool:
    now = datetime.now()
    recent_requests = [t for t in ip_data["request_times"] if now - t <= timedelta(seconds=window_sec)]
    return len(recent_requests) >= max_requests

def calculate_risk_score():
    pass


def evaluate_action():
    pass