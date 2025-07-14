from reader import read_static_log_file
from parser import parse_log_line
from updater import update_ip_record    

log_lines = read_static_log_file('/home/aysenur/projects/nginx_analyzer/nginx-access-example.log')
ip_data = {}

for line in log_lines:
    parsed_line = parse_log_line(line)
    update_ip_record(parsed_line, ip_data)

for ip, data in ip_data.items():
    print(f"IP: {ip}")
    print(f"  Request Times: {data['request_times']}")
    print(f"  User Agents: {data['user_agents']}")
    print(f"  Request Count: {data['request_count']}")
    print(f"  Status Codes: {data['status_codes']}")
    print(f"  Is Bot: {data['is_bot']}")
    print(f"  Last Seen: {data['last_seen']}\n")
    print("-" * 40)
    print()
