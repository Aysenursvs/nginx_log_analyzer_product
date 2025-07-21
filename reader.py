
import time
import json
import os

def follow_log_file(file_path):
    with open(file_path, "r") as f:
        for line in f:
            yield line
        while True:
            line = f.readline()
            if not line:
                print("Bekleniyor...")
                f.seek(0, os.SEEK_CUR) 
                time.sleep(0.5)
                continue
            
            yield line


#Read static log file

def read_static_log_file(file_path):
    """
    Reads a static log file and returns its content.
    
    :param file_path: Path to the log file
    :return: Content of the log file as a string
    """
    try:
        with open(file_path, 'r') as file:
            for line in file:
                yield line
    except FileNotFoundError:
        raise FileNotFoundError(f"Error: The file {file_path} does not exist.")
    except Exception as e:
        raise Exception(f"An error occurred while reading the file: {e}")
    
def total_lines_in_file(file_path):
    with open(file_path, 'r') as f:
        total_lines = sum(1 for _ in f)
    return total_lines

def load_ip_location_cache(file_path="ip_location_cache_prefix.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

def load_prefix_counter(file_path="prefix_counter.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

