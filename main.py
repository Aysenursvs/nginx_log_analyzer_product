from reader import read_static_log_file
from parser import parse_log_line
from updater import update_ip_record, print_record, update_bot_status
from anlyzer import is_bot_by_user_agent   


log_lines = read_static_log_file('/home/aysenur/projects/nginx_analyzer/nginx-access-example.log')
ip_datas = {}

for line in log_lines:
    parsed_line = parse_log_line(line)
    ip_data = update_ip_record(parsed_line, ip_datas)
    bot_status = is_bot_by_user_agent(ip_data["user_agents"])
    update_bot_status(ip_data, bot_status)

print_record(ip_datas)



