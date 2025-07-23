from reader import read_static_log_file, follow_log_file, load_ip_location_cache, total_lines_in_file, load_prefix_counter
from saver import save_ip_data_to_file, save_single_ip_data, save_bad_lines_to_file, save_ip_location_cache, save_prefix_counter,save_warning_to_file
from parser import parse_log_line
from updater import update_ip_record,update_ip_status
from actions import give_warning
from variables import source_file_path_real, target_file_path_real, source_file_path_example, target_file_path_example, ip_location_cache_file_path, prefix_counter_file_path, log_results_file_path
from simulator import simulate_logging
from tqdm import tqdm
from threading import Thread




# Initialize DATA STRUCTURES
ip_datas = {}   # Dictionary to hold IP data. IP addresses are keys and their data are values.
bad_lines = []  # List to hold bad lines (lines that could not be parsed)

# Load IP location cache
ip_location_cache = load_ip_location_cache(ip_location_cache_file_path)
# Load prefix counter
prefix_counter = load_prefix_counter(prefix_counter_file_path)

# Get total number of lines for progress bar
total_lines = total_lines_in_file(source_file_path_real)

#sim_thread = Thread(target=simulate_logging, args=(source_file_path, target_file_path))
#sim_thread.start()

# Read log files
log_lines = read_static_log_file(source_file_path_real)     #read static log file
log_lines_dynamic = follow_log_file(target_file_path_real)  #follow dynamic log file

# This function processes the log lines, updates IP records, calculates risk scores, and gives warnings based on the actions.
# It saves the results to files periodically and prints the actions and risk scores.
def run(log_lines, total_lines, ip_location_cache, ip_datas, bad_lines):
    for line_number, line in enumerate(tqdm(log_lines, total=total_lines, desc="Processing log lines"), start=1):
        
        # Parse the log line
        # If the line is not valid, it will be added to bad_lines list.
        parsed_line = parse_log_line(line)
        if parsed_line is None:
            bad_lines.append((line_number, line))
            continue

        # Update IP record with parsed line data
        ip_data = update_ip_record(parsed_line, ip_datas, ip_location_cache, prefix_counter)

        # Update IP status based on the ip_data
        update_ip_status(ip_data, prefix_counter)

        # Give warning based on the action of the IP data
        warning = give_warning(ip_data, ip=parsed_line.get('ip'))
        print(warning) if warning else None
        save_warning_to_file(warning, line_number)

        #save_single_ip_data('/home/aysenur/projects/nginx_analyzer/ip_datas_real_static.json', parsed_line.get('ip'), ip_data)

        # Save results to files periodically
        if line_number % 1000 == 0:
            save_ip_location_cache(ip_location_cache)
            save_ip_data_to_file(log_results_file_path, ip_datas)
            #save_prefix_counter(prefix_counter)
            save_bad_lines_to_file(bad_lines)

        print(f"[Line {line_number}]:IP: {parsed_line.get('ip')} - Action: {ip_data['action']} - Risk Score: {ip_data['risk_score']}")


# If you want to analyze a static log file;
# use "log_lines" variable and update the file path variable source_file_path_real in variables.py for static log file.
# If you want to follow a dynamic log file;
# use "log_lines_dynamic" variable and update the file path variable source_file_path_real in variables.py for dynamic log file.
# And also update log_results_file_path in variables.py to save the results.
# You can change all file paths in variables.py to your desired paths.
# You can also use the simulator to simulate logging.
# Uncomment the sim_thread line to start the simulator. This simulator is for dynamic log file and test purposes.

run(log_lines_dynamic, total_lines, ip_location_cache, ip_datas, bad_lines)





