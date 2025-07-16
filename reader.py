
import time
import json
import os

def follow_log_file(file_path):
    """
    Yields all existing lines in the file, then continuously yields new lines as they are added.
    Like `tail -f` but includes initial content.
    """
    with open(file_path, "r") as f:
        # İlk olarak dosyada var olan tüm satırları oku
        for line in f:
            yield line
        # Sonra yeni satır geldikçe oku
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
    
def total_lines_in_file(file_path):
    with open(file_path, 'r') as f:
        total_lines = sum(1 for _ in f)
    return total_lines

def load_ip_location_cache(file_path="ip_location_cache.json"):
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            return json.load(f)
    return {}

