
import time
import json
import os


# This function reads a log file line by line and yields each line.
# It first reads the file if there are existing lines, then continues to read new lines as they are added.
def follow_log_file(file_path):
    try:
        with open(file_path, "r") as f:
            for line in f:
                yield line
            while True:
                try:
                    line = f.readline()
                    if not line:
                        print("Bekleniyor...")
                        f.seek(0, os.SEEK_CUR)
                        time.sleep(0.5)
                        continue
                    yield line
                except Exception as e:
                    print(f"An error occurred while reading the file: {e}")
                    time.sleep(1)
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while opening the file: {e}")

#This function reads a static log file and yields each line.
#Static log file means new log lines are not added to this file.
def read_static_log_file(file_path):
    try:
        with open(file_path, 'r') as file:
            for line in file:
                yield line
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")

# This function counts the total number of lines in a file.
# It uses in the main.py file to get the total number of lines for the progress bar.   
def total_lines_in_file(file_path):
    with open(file_path, 'r') as f:
        total_lines = sum(1 for _ in f)
    return total_lines

# This function loads the IP location cache from a file.
# If the file does not exist or is empty, it returns an empty dictionary.
# It is used in the main.py file to load the IP location cache.
def load_ip_location_cache(file_path="ip_location_cache_prefix.json"):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

# This function loads the prefix counter from a file.
# If the file does not exist or is empty, it returns an empty dictionary.
# It is used in the main.py file to load the prefix counter.
def load_prefix_counter(file_path="prefix_counter.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

