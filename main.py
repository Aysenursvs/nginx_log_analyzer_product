from reader import read_static_log_file
from saver import save_ip_data_to_file
from parser import parse_log_line
from updater import update_ip_record, print_record, update_ip_status



log_lines = read_static_log_file('/home/aysenur/projects/nginx_analyzer/nginx-access-example.log')
ip_datas = {}

for line in log_lines:
    parsed_line = parse_log_line(line)
    ip_data = update_ip_record(parsed_line, ip_datas)
    update_ip_status(ip_data)

save_ip_data_to_file('/home/aysenur/projects/nginx_analyzer/ip_datas.json', ip_datas)

print_record(ip_datas)



