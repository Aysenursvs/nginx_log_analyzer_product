from slack_sdk import WebClient 
import os
import logging
from variables import slack_channel, slack_channel_id, slack_token





def send_slack_message(message):
    try:
        client = WebClient(token=slack_token)
        # Mesaj gönder
        client.chat_postMessage(
            channel=slack_channel,
            text=message,
            username="Nginx Analyzer Bot"
        )
        
    except Exception as e:
        logging.error(f"Slack message error: {e}")

def send_slack_file(file_path):
    try:
        client = WebClient(token=slack_token)
        if file_path and os.path.exists(file_path):
            response = client.files_upload_v2(
                channel=slack_channel_id,
                file=file_path,
                title="Nginx Log Analysis Results",
                filename=os.path.basename(file_path)
            )
            logging.info(f"File uploaded successfully: {response['file']['name']}")
    except Exception as e:
        logging.error(f"Slack file upload error: {e}")
    