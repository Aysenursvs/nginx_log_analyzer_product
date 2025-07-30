from slack_app import send_slack_message, send_slack_file
from variables import slack_channel, slack_channel_id, slack_token
#This file contains functions to analyze IP data and determine actions based on risk scores.

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

def give_notification(warning_message, file_path):
    send_slack_message(warning_message, slack_channel, slack_token)
    send_slack_file(file_path, slack_channel_id, slack_token)

def block_ip():
    pass