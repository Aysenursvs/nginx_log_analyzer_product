import logging
from datetime import datetime
from slack_app import send_slack_message, send_slack_file
from variables import human


#This function gives warnings based on the action of the IP data.
#If the action is "review", it prints a review warning message and sets the review_warning flag to True.
#If the action is "block", it prints a block warning message and sets the block_warning flag to True.
#The warning messages include the IP address, action, and risk score.
def give_warning(ip_data:dict, ip) -> str:
    warning = ""
    if ip_data["action"] != "normal":
        if ip_data['action'] == "review" and not ip_data["review_warning"]:
            warning = f"Review Warning: IP {ip} has action '{ip_data['action']}' with risk score {ip_data['risk_score']}."
            ip_data["review_warning"] = True
        if ip_data['action'] == "block" and not ip_data["block_warning"]:
            warning = f"Block Warning: IP {ip} has action '{ip_data['action']}' with risk score {ip_data['risk_score']}."
            ip_data["block_warning"] = True
    return warning


# This function formats the IP data into a readable string format for Slack messages.
# It includes basic info, security assessment, risk analysis, and request details.
# It handles datetime objects and ensures that the output is user-friendly.
def format_ip_info(ip_data: dict, ip_address: str) -> str:
    """
    IP bilgilerini okunabilir formatta string'e çevirir
    """
    try:
        # Datetime objelerini string'e çevir
        last_seen = ip_data.get('last_seen')
        if isinstance(last_seen, datetime):
            last_seen_str = last_seen.strftime('%Y-%m-%d %H:%M:%S')
        else:
            last_seen_str = str(last_seen)
        
        # Okunabilir format
        formatted_info = f"""
🔍 **IP Analysis Report: {ip_address}**
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📊 **Basic Info:**
   • Request Count: {ip_data.get('request_count', 0)}
   • Last Seen: {last_seen_str}
   • Country: {ip_data.get('country', 'Unknown')}
   • City: {ip_data.get('city', 'Unknown')}

🤖 **Security Assessment:**
   • Is Bot: {ip_data.get('is_bot')}
   • Is Suspicious: {ip_data.get('is_suspicious')}
   • Rate Limit Exceeded: {ip_data.get('is_limit_exceeded')}

⚠️ **Risk Analysis:**
   • Risk Score: {ip_data.get('risk_score', 0)}
        - Bot Risk: {ip_data.get('bot_risk', 0)}
        - Suspicious Risk: {ip_data.get('suspicious_risk', 0)}
        - Rate Limit Risk: {ip_data.get('risk_components', {}).get('rate_limit', 0)}
        - Prefix Risk: {ip_data.get('risk_components', {}).get('prefix', 0)}
        - Location Risk: {ip_data.get('risk_components', {}).get('location', 0)}
   • Action: {ip_data.get('action', 'normal').upper()}


📈 **Request Details:**
   • Status Codes: {dict(ip_data.get('status_codes', {}))}
   • User Agents: {ip_data.get('user_agents', [])} 
   • Network Prefix: {ip_data.get('prefix', 'Unknown')}
        """
        
        return formatted_info.strip()
        
    except Exception as e:
        logging.error(f"Error formatting IP info: {e}")
        return f"IP: {ip_address} - Error formatting data"

def block_ip(ip_address, reason=None):
    
    pass


# This function handles the warning notification process.
# It checks if the warning message is present and whether human intervention is enabled.
# If human intervention is enabled, it sends a Slack message with the warning and formatted IP info
# and uploads the file containing the IP data.
# If human intervention is not enabled, it blocks the IP address.
def handle_warning_notification(warning_message, ip_data, file_path, ip_address):
    if not warning_message:
        return
    
    is_human_enabled = human
    
    if is_human_enabled:
        send_slack_message(warning_message)
        formatted_info = format_ip_info(ip_data, ip_address)
        send_slack_message(formatted_info)
        send_slack_file(file_path)
        logging.info(f"Human notification sent for IP: {ip_address}")
    else:
        block_ip(ip_address, warning_message)
        logging.info(f"Automatic blocking initiated for IP: {ip_address}")

