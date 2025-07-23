import json
import os

# This function saves IP data to a file.
# It takes a file path and a dictionary of IP data as arguments.
# If the file does not exist, it creates a new file and writes the data.
# If the file exists, it overwrites the existing data with the new data.
# The data is saved in JSON format with indentation for readability.
# It is used in the main.py file to save the IP data after analyzing it. 
# Each 1000 lines processed, it saves the IP data to the file.
def save_ip_data_to_file(file_path, ip_datas):
    try:
        with open(file_path, 'w') as f:
            json.dump(ip_datas, f, default=str, indent=4)
    except Exception as e:
        print(f"Error while saving data: {e}")

# This function saves a single IP's data to a file.
# It reads the existing data from the file, updates the data for the given IP,
# and then writes the updated data back to the file.
# It is used in the main.py file to save the IP data after analyzing it in each iteration.
def save_single_ip_data(file_path, ip, ip_data):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # Update the data for the given IP
    data[ip] = ip_data

    # Write the updated data back to the file
    with open(file_path, 'w') as f:
        json.dump(data, f, default=str, indent=4)
   
# This function saves bad log lines to a file.
# Bad line example: [Line 30729]: 185.67.33.199 - - [15/Jul/2025:02:05:54 +0300] "" 400 0 "-" "-"
# In this example, the request part is empty, which is considered a bad line.
def save_bad_lines_to_file(bad_lines):
    if not bad_lines:
        return
    
    with open("bad_log_lines.txt", "w") as f:
        for line_number, line_content in bad_lines:
            f.write(f"[Line {line_number}]: {line_content}")

# This function saves the IP location cache to a file.
# It takes a cache dictionary and a file path as arguments.
# If the file does not exist, it creates a new file and writes the cache data.
# If the file exists, it overwrites the existing cache data with the new data.
# The cache data is saved in JSON format with indentation for readability.
def save_ip_location_cache(cache, file_path="ip_location_cache_prefix.json"):
    with open(file_path, "w") as f:
        json.dump(cache, f, indent=4)
    
# This function saves the prefix counter to a file.
# It takes a counter dictionary and a file path as arguments.
# If the file does not exist, it creates a new file and writes the counter data.
# If the file exists, it overwrites the existing counter data with the new data.
# The counter data is saved in JSON format with indentation for readability.
def save_prefix_counter(counter, file_path="prefix_counter.json"):
    with open(file_path, "w") as f:
        json.dump(counter, f, indent=4)