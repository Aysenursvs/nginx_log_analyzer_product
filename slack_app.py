from slack_sdk import WebClient 
import os
import logging



def client(slack_token):
    return WebClient(token=slack_token)

def send_slack_message(message, channel, slack_token):
    try:
        client = client(slack_token)
        # Mesaj gönder
        client.chat_postMessage(
            channel=channel,
            text=message,
            username="Nginx Analyzer Bot"
        )
        
    except Exception as e:
        logging.error(f"Slack message error: {e}")

def send_slack_file(file_path, channel_id, slack_token):
    try:
        client = client(slack_token)
        # Dosya gönder
        if file_path and os.path.exists(file_path):
            response = client.files_upload(
                channels=channel_id,
                file=file_path,
                title="Nginx Log Analysis Results",
                filename=os.path.basename(file_path)
            )
            logging.info(f"File uploaded successfully: {response['file']['name']}")
    except Exception as e:
        logging.error(f"Slack file upload error: {e}")
    