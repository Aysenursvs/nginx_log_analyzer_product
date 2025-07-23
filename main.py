from reader import read_static_log_file, follow_log_file, load_ip_location_cache, total_lines_in_file, load_prefix_counter
from saver import save_ip_data_to_file, save_single_ip_data, save_bad_lines_to_file, save_ip_location_cache, save_prefix_counter
from parser import parse_log_line
from updater import update_ip_record,update_ip_status
from actions import give_warning
from variables import source_file_path_real, target_file_path_real, source_file_path_example, target_file_path_example, ip_location_cache_file_path
from simulator import simulate_logging
from tqdm import tqdm
from threading import Thread





ip_datas = {}
bad_lines = []

# Load IP location cache
ip_location_cache = load_ip_location_cache(ip_location_cache_file_path)
prefix_counter = load_prefix_counter()

# Get total number of lines for progress bar
total_lines = total_lines_in_file(source_file_path_real)

#sim_thread = Thread(target=simulate_logging, args=(source_file_path, target_file_path))
#sim_thread.start()

# Read log files
log_lines = read_static_log_file(source_file_path_real)
log_lines_dynamic = follow_log_file(target_file_path_real)

def run(log_lines, total_lines, ip_location_cache, ip_datas, bad_lines):
    for line_number, line in enumerate(tqdm(log_lines, total=total_lines, desc="Processing log lines"), start=1):
        parsed_line = parse_log_line(line)
        if parsed_line is None:
            bad_lines.append((line_number, line))
            continue
        ip_data = update_ip_record(parsed_line, ip_datas, ip_location_cache, prefix_counter)
        
        update_ip_status(ip_data, prefix_counter)

        give_warning(ip_data, ip=parsed_line.get('ip'))

        #save_single_ip_data('/home/aysenur/projects/nginx_analyzer/ip_datas_real_static.json', parsed_line.get('ip'), ip_data)
        
        if line_number % 1000 == 0:
            save_ip_location_cache(ip_location_cache)
            save_ip_data_to_file('/home/aysenur/projects/nginx_analyzer/ip_datas_real_dynamic_location.json', ip_datas)
            save_prefix_counter(prefix_counter)
            save_bad_lines_to_file(bad_lines)
        


run(log_lines_dynamic, total_lines, ip_location_cache, ip_datas, bad_lines)





