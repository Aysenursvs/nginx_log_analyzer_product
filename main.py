from reader import read_static_log_file, follow_log_file, load_ip_location_cache, load_prefix_counter
from saver import save_ip_data_to_file,save_bad_lines_to_file, save_ip_location_cache, save_prefix_counter,save_warning_to_file
from parser import parse_log_line
from updater import update_ip_record,update_ip_status, update_warning
from actions import give_warning
from variables import source_file_path_real, target_file_path_real, ip_location_cache_file_path, prefix_counter_file_path, log_results_file_path, bad_lines_file_path, warnings_file_path
import logging


# Configure logging: Sets up logging to write INFO level logs and above
# to 'analyzer.log' file with timestamp, log level and message format
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("analyzer.log")
    ]
)




# Initialize DATA STRUCTURES
ip_datas = {}   # Dictionary to hold IP data. IP addresses are keys and their data are values.
bad_lines = {}  # Dictionary to hold bad lines (lines that could not be parsed)
warnings = {}  # Dictionary to hold warnings (IP addresses as key and warning message as value)

# Load IP location cache
ip_location_cache = load_ip_location_cache(ip_location_cache_file_path)
# Load prefix counter
prefix_counter = load_prefix_counter(prefix_counter_file_path)


# Read log files
log_lines = read_static_log_file(source_file_path_real)     #read static log file
log_lines_dynamic = follow_log_file(target_file_path_real)  #follow dynamic log file

# This function processes the log lines, updates IP records, calculates risk scores, and gives warnings based on the actions.
# It saves the results to files periodically and prints the actions and risk scores.
def run(log_lines,ip_location_cache, ip_datas, bad_lines):
    for line_number, line in enumerate(log_lines, start=1):

        # Parse the log line
        # If the line is not valid, it will be added to bad_lines list.
        parsed_line = parse_log_line(line)
        if parsed_line is None:
            bad_lines[line_number] = line
            continue

        # Update IP record with parsed line data
        ip_data = update_ip_record(parsed_line, ip_datas, ip_location_cache, prefix_counter)

        # Update IP status based on the ip_data
        update_ip_status(ip_data, prefix_counter)

        # Give warning based on the action of the IP data
        warning = give_warning(ip_data, ip=parsed_line.get('ip'))
        update_warning(warnings, warning, parsed_line.get('ip'), line_number)
        save_warning_to_file(warnings, warnings_file_path)

        

        # Save results to files periodically
        if line_number % 1000 == 0:
            save_ip_location_cache(ip_location_cache, ip_location_cache_file_path)
            save_ip_data_to_file(ip_datas, log_results_file_path)
            save_prefix_counter(prefix_counter, prefix_counter_file_path)
            save_bad_lines_to_file(bad_lines, bad_lines_file_path)


# If you want to analyze a static log file;
# use "log_lines" variable and update the file path variable source_file_path_real in variables.py for static log file.
# If you want to follow a dynamic log file;
# use "log_lines_dynamic" variable and update the file path variable source_file_path_real in variables.py for dynamic log file.
# And also update log_results_file_path in variables.py to save the results.
# You can change all file paths in variables.py to your desired paths.


if __name__ == "__main__":
    run(log_lines_dynamic, ip_location_cache, ip_datas, bad_lines)






