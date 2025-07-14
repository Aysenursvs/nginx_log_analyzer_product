from reader import read_static_log_file
from parser import parse_log_line

log_lines = read_static_log_file('/home/aysenur/projects/nginx_analyzer/nginx-access-example.log')

for line in log_lines:
    parsed_line = parse_log_line(line)
    if parsed_line:
        print(parsed_line)
