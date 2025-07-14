from reader import read_static_log_file

log_lines = read_static_log_file('/home/aysenur/projects/nginx_analyzer/nginx-access-example.log')

for line in log_lines:
    print(line)