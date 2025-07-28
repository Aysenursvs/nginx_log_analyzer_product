import json
import os
import logging


# This function save dictionary to JSON file
def write_json(data, file_path):
   
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
        
    except Exception as e:
        logging.error(f"Failed to write JSON to {file_path}: {e}")

# This function loads JSON data from a file, returning an empty dictionary if the file doesn't exist or is corrupted
def load_existing_json(file_path):
    
    if os.path.exists(file_path):
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.warning(f"Corrupted JSON detected at {file_path}, starting fresh.")
            return {}
    return {}

# This function saves IP data to a file.
# It takes a file path and a dictionary of IP data as arguments.
# If the file does not exist, it creates a new file and writes the data.
# If the file exists, it overwrites the existing data with the new data.
# The data is saved in JSON format with indentation for readability.
# It is used in the main.py file to save the IP data after analyzing it. 
# Each 1000 lines processed, it saves the IP data to the file.
def save_ip_data_to_file(ip_datas, file_path):
    try:
        with open(file_path, 'w') as f:
            json.dump(ip_datas, f, default=str, indent=4)
    except Exception as e:
        logging.error(f"Failed to write JSON to {file_path}: {e}")
    

# This function saves a single IP's data to a file.
# It reads the existing data from the file, updates the data for the given IP,
# and then writes the updated data back to the file.
# It is used in the main.py file to save the IP data after analyzing it in each iteration.
def save_single_ip_data(file_path, ip, ip_data):
    try:
        data = load_existing_json(file_path)
        data[ip] = ip_data
        with open(file_path, 'w') as f:
            json.dump(data, f, default=str, indent=4)
    except Exception as e:
        logging.error(f"Failed to save single IP data for {ip}: {e}")


   
# This function saves bad log lines to a file.
# Bad line example: [Line 30729]: 185.67.33.199 - - [15/Jul/2025:02:05:54 +0300] "" 400 0 "-" "-"
# In this example, the request part is empty, which is considered a bad line.
def save_bad_lines_to_file(bad_lines, file_path="bad_lines.json"):
    if not bad_lines:
        return
    # Save as JSON file
    write_json(bad_lines, file_path)

# This function saves the IP location cache to a file.
# It takes a cache dictionary and a file path as arguments.
# If the file does not exist, it creates a new file and writes the cache data.
# If the file exists, it overwrites the existing cache data with the new data.
# The cache data is saved in JSON format with indentation for readability.
def save_ip_location_cache(cache, file_path="ip_location_cache_prefix.json"):
    write_json(cache, file_path)
    
# This function saves the prefix counter to a file.
# It takes a counter dictionary and a file path as arguments.
# If the file does not exist, it creates a new file and writes the counter data.
# If the file exists, it overwrites the existing counter data with the new data.
# The counter data is saved in JSON format with indentation for readability.
def save_prefix_counter(counter, file_path="prefix_counter.json"):
    write_json(counter, file_path)

# This function saves a warning message to a specified text file.
# It takes a warning message, line number, and file path as arguments.
# If the warning message is empty, the function returns early.
# The warning is appended to the file with the format "[Line X] warning message".
# If there's an error during the file operation, it logs the error.
def save_warning_to_file(warning, line_number, file_path="warnings.txt"):
    if not warning:
        return
    with open(file_path, "a") as f:
        f.write(f"[Line {line_number}]: {warning}\n")