from reader import read_static_log_file, follow_log_file, load_ip_location_cache, total_lines_in_file, load_prefix_counter
from saver import save_ip_data_to_file, save_single_ip_data, save_bad_lines_to_file, save_ip_location_cache, save_prefix_counter
from parser import parse_log_line
from updater import update_ip_record, print_record, update_ip_status
from actions import give_warning
from simulator import simulate_logging
import os
from tqdm import tqdm
from threading import Thread



log_file_path = '/home/aysenur/projects/nginx_analyzer/nginx.vhost.access.log'
log_file_path2 = '/home/aysenur/projects/nginx_analyzer/nginx-access-example.log'
log_file_path3 = '/home/aysenur/projects/nginx_analyzer/nginx-access-example-copy.log'
source_file_path = '/home/aysenur/projects/nginx_analyzer/nginx-source-log.log'
target_file_path = '/home/aysenur/projects/nginx_analyzer/nginx-target-log.log'
ip_datas = {}
bad_lines = []

# Load IP location cache
ip_location_cache = load_ip_location_cache()
prefix_counter = load_prefix_counter()

# Get total number of lines for progress bar
total_lines = total_lines_in_file(log_file_path)

sim_thread = Thread(target=simulate_logging, args=(log_file_path, log_file_path2))
sim_thread.start()

# Read log files
log_lines = read_static_log_file(log_file_path)
log_lines_dynamic = follow_log_file(log_file_path2)

def run(log_lines, total_lines, ip_location_cache, ip_datas, bad_lines):
    for line_number,line in enumerate(tqdm(log_lines, total=total_lines, desc="Processing log lines"), start=1):
        parsed_line = parse_log_line(line)
        if parsed_line is None:
            bad_lines.append((line_number, line))
            continue
        ip_data = update_ip_record(parsed_line, ip_datas, ip_location_cache, prefix_counter)
        
        update_ip_status(ip_data, prefix_counter)

        give_warning(ip_data, ip=parsed_line.get('ip'))

        if line_number % 1000 == 0:
            
            save_ip_location_cache(ip_location_cache)
           
            save_single_ip_data('/home/aysenur/projects/nginx_analyzer/ip_datas_real_dynamic.json', parsed_line.get('ip'), ip_data)
        
            #save_prefix_counter(prefix_counter)
            save_bad_lines_to_file(bad_lines)

try:
    run(log_lines_dynamic, total_lines, ip_location_cache, ip_datas, bad_lines)
except KeyboardInterrupt:
    print("Stopped by user")

#save_ip_data_to_file('/home/aysenur/projects/nginx_analyzer/ip_datas.json', ip_datas)

#print_record(ip_datas)



