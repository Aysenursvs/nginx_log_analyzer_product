## main.py ##
#File paths:

#Source files are static log files. that means new log lines are not added to them.
#Target files are dynamic log files. that means new log lines are added to them.
source_file_path_real = '/home/aysenur/projects/nginx_analyzer/nginx.vhost.access.log'
target_file_path_real = '/home/aysenur/projects/nginx_analyzer/nginx-access-example.log'


#load_ip_location_cache function loads IP location data from this file if it exists.
ip_location_cache_file_path = '/home/aysenur/projects/nginx_analyzer/ip_location_cache_prefix.json'
#load_prefix_counter function loads prefix counter data from this file if it exists.
prefix_counter_file_path = '/home/aysenur/projects/nginx_analyzer/prefix_counter.json'
#bad_lines_file_path is used to save bad log lines.
bad_lines_file_path = '/home/aysenur/projects/nginx_analyzer/bad_lines.json'
#warnings_file_path is used to save warnings.
warnings_file_path = '/home/aysenur/projects/nginx_analyzer/warnings.txt'

#save_ip_data_to_file function saves ip data to this file
log_results_file_path = '/home/aysenur/projects/nginx_analyzer/real_logs/ip_datas_real_dynamic_location.json'





## updater.py ##

# check_request_count function (in the analyzer.py but called in the updater.py) checks request count against this threshold.
# default value is 10000 (in the function)
# This value is used to determine if the request count is suspicious. 
# If the request count is greater than or equal to this value, it is considered suspicious.
# is_suspicious flag is set to True in the update_ip_status function (in the updater.py) if the request count is suspicious.
# You can change this value here.
request_count_threshold = 1000

# is_rate_limit_exceeded function (in the analyzer.py but called in the updater.py) checks rate limit against this threshold.
# default value for window_sec is 60 (in the function)
# default value for max_requests is 100 (in the function)
# These values are used to determine if the rate limit is exceeded.
# If the number of requests in the last 60 seconds is greater than or equal to 100, it is considered rate limit exceeded.
# is_limit_exceeded flag is set to True in the update_ip_status function (in the updater.py) if the rate limit is exceeded.
# You can change this value here.
rate_limit_window_sec = 60
max_requests = 2400

# update_action_by_risk_score function (in the updater.py) uses these risk scores to determine actions.
# These values are used to determine if the IP should be blocked or reviewed.
# If the risk score is greater than or equal to block_risk_score, the action is set to "block",
# then give_warning function prints a warning message and sets the block_warning flag to True.
# If the risk score is greater than or equal to review_risk_score, the action is set to "review",
# then give_warning function prints a warning message and sets the review_warning flag to True.
# You can change these values here.
 
block_risk_score = 70
review_risk_score = 40

## analyzer.py ##
# If you want to change the risk scores for bot, suspicious, rate limit, prefix, and location,
# you can change these values in the analyzer.py file.
# Determine the risk scores and thresholds in the "analyze and calculate risk scores part" in the analyzer.py file.



