import os
from dotenv import load_dotenv
from pathlib import Path

# Define the path to the .env file
env_path = Path('.') / '.env'

# Load environment variables from .env file
load_dotenv(env_path)

## main.py ##
#File paths:

#Source files are static log files. that means new log lines are not added to them.
#Target files are dynamic log files. that means new log lines are added to them.
source_file_path_real = os.getenv("SOURCE_FILE_PATH_REAL")
target_file_path_real = os.getenv("TARGET_FILE_PATH_REAL")


#load_ip_location_cache function loads IP location data from this file if it exists.
ip_location_cache_file_path = os.getenv("IP_LOCATION_CACHE_FILE_PATH")
#load_prefix_counter function loads prefix counter data from this file if it exists.
prefix_counter_file_path = os.getenv("PREFIX_COUNTER_FILE_PATH")
#bad_lines_file_path is used to save bad log lines.
bad_lines_file_path = os.getenv("BAD_LINES_FILE_PATH")
#warnings_file_path is used to save warnings.
warnings_file_path = os.getenv("WARNINGS_FILE_PATH")
#save_ip_data_to_file function saves ip data to this file
log_results_file_path = os.getenv("LOG_RESULTS_FILE_PATH")

# This file is used to save the results of the analysis.
logging_file_path = os.getenv("LOGGING_FILE_PATH")

# This variable is used for human interaction.
# If you want to enable human interaction, set this variable to "true" in the .env file.
# If you want to disable human interaction, set this variable to "false" in the .env file.
human = os.getenv("HUMAN")

## actions.py ##

# This variable is used to send notifications to Slack.
slack_channel = os.getenv("SLACK_CHANNEL")
slack_channel_id = os.getenv("SLACK_CHANNEL_ID")
slack_token = os.getenv("SLACK_TOKEN")


## updater.py ##

API_KEY = os.getenv("IPINFO_API_KEY")

# check_request_count function (in the analyzer.py but called in the updater.py) checks request count against this threshold.
# default value is 10000 (in the function)
# This value is used to determine if the request count is suspicious. 
# If the request count is greater than or equal to this value, it is considered suspicious.
# is_suspicious flag is set to True in the update_ip_status function (in the updater.py) if the request count is suspicious.
# You can change this value here.
request_count_threshold = int(os.getenv("REQUEST_COUNT_THRESHOLD", 10000))

# is_rate_limit_exceeded function (in the analyzer.py but called in the updater.py) checks rate limit against this threshold.
# default value for window_sec is 60 (in the function)
# default value for max_requests is 100 (in the function)
# These values are used to determine if the rate limit is exceeded.
# If the number of requests in the last 60 seconds is greater than or equal to 100, it is considered rate limit exceeded.
# is_limit_exceeded flag is set to True in the update_ip_status function (in the updater.py) if the rate limit is exceeded.
# You can change this value here.
rate_limit_window_sec = int(os.getenv("RATE_LIMIT_WINDOW_SEC", 60))
max_requests = int(os.getenv("MAX_REQUESTS", 2400))

# update_action_by_risk_score function (in the updater.py) uses these risk scores to determine actions.
# These values are used to determine if the IP should be blocked or reviewed.
# If the risk score is greater than or equal to block_risk_score, the action is set to "block",
# then give_warning function prints a warning message and sets the block_warning flag to True.
# If the risk score is greater than or equal to review_risk_score, the action is set to "review",
# then give_warning function prints a warning message and sets the review_warning flag to True.
# You can change these values here.

block_risk_score = int(os.getenv("BLOCK_RISK_SCORE", 70))
review_risk_score = int(os.getenv("REVIEW_RISK_SCORE", 40))

## analyzer.py ##
# If you want to change the risk scores for bot, suspicious, rate limit, prefix, and location,
# you can change these values in the analyzer.py file.
# Determine the risk scores and thresholds in the "analyze and calculate risk scores part" in the analyzer.py file.



