from reader import read_static_log_file, follow_log_file
from saver import save_ip_data_to_file, save_single_ip_data
from parser import parse_log_line
from updater import update_ip_record, print_record, update_ip_status
import os
from tqdm import tqdm



log_file_path = '/home/aysenur/projects/nginx_analyzer/nginx.vhost.access.log'
ip_datas = {}

# Get total number of lines for progress bar
with open(log_file_path, 'r') as f:
    total_lines = sum(1 for _ in f)

log_lines = read_static_log_file(log_file_path)

for line in tqdm(log_lines, total=total_lines, desc="Processing log lines"):
    parsed_line = parse_log_line(line)
    ip_data = update_ip_record(parsed_line, ip_datas)
    update_ip_status(ip_data)

    save_single_ip_data('/home/aysenur/projects/nginx_analyzer/ip_datas_single.json', parsed_line.get('ip'), ip_data)

save_ip_data_to_file('/home/aysenur/projects/nginx_analyzer/ip_datas.json', ip_datas)

print_record(ip_datas)



