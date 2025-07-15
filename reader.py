
import time
import json
import os

def follow_log_file(file_path):
    """
    Continuously yields new lines as they are added to the file.
    Like `tail -f`.
    """
    with open(file_path, "r") as f:
        f.seek(0, 2)  # Go to end of file
        while True:
            line = f.readline()
            if not line:
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
    

def load_ip_location_cache(file_path="ip_location_cache.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

