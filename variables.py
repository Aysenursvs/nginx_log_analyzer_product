## main.py ##
#File paths:

#Source files are static log files. that means new log lines are not added to them.
#Target files are dynamic log files. that means new log lines are added to them.
source_file_path_real = '/home/aysenur/projects/nginx_analyzer/nginx.vhost.access.log'
target_file_path_real = '/home/aysenur/projects/nginx_analyzer/nginx-access-example.log'

source_file_path_example = '/home/aysenur/projects/nginx_analyzer/nginx-source-log.log'
target_file_path_example = '/home/aysenur/projects/nginx_analyzer/nginx-target-log.log'

#load_ip_location_cache function loads IP location data from this file if it exists.
ip_location_cache_file_path = '/home/aysenur/projects/nginx_analyzer/ip_location_cache_prefix.json'
#load_prefix_counter function loads prefix counter data from this file if it exists.
prefix_counter_file_path = '/home/aysenur/projects/nginx_analyzer/prefix_counter.json'

#save_ip_data_to_file function saves ip data to this file
log_results_file_path = '/home/aysenur/projects/nginx_analyzer/real_logs/ip_datas_real_dynamic_location.json'



### for updater functions
block_risk_score = 80
review_risk_score = 50

### for analyzer functions
## check_request_count
request_count_threshold = 150

##is_rate_limit_exceeded 
rate_limit_threshold = 100
rate_limit_window_sec = 60
max_requests = 100