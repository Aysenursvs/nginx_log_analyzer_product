
import time
import json
import os
import logging


# This function reads a log file line by line and yields each line.
# It first reads the file if there are existing lines, then continues to read new lines as they are added.
def follow_log_file(file_path):
    
    try:
        f = open(file_path, "r")
        current_inode = os.fstat(f.fileno()).st_ino

        # Read all existing lines in the file and yield them
        for line in f:
            yield line

        # After reading to the last line, follow new lines
        while True:
            line = f.readline()

            if line:
                yield line
            else:
                # Check if file rotation occurred
                try:
                    if os.stat(file_path).st_ino != current_inode:
                        logging.info("Log rotation detected. Reopening log file...")
                        f.close()
                        f = open(file_path, "r")
                        current_inode = os.fstat(f.fileno()).st_ino
                        # Read any accumulated lines in the new file
                        for line in f:
                            yield line
                except FileNotFoundError:
                    logging.warning("Log file not found, waiting for re-creation...")
                    time.sleep(1)
                    continue

                time.sleep(0.5)
    except Exception as e:
        logging.error(f"Error in follow_log_file: {e}")
        raise

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


# This function loads the IP location cache from a file.
# If the file does not exist or is empty, it returns an empty dictionary.
# It is used in the main.py file to load the IP location cache.
def load_ip_location_cache(file_path="ip_location_cache_prefix.json"):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.warning(f"Corrupted JSON in {file_path}, returning empty cache.")
            return {}
    return {}

# This function loads the prefix counter from a file.
# If the file does not exist or is empty, it returns an empty dictionary.
# It is used in the main.py file to load the prefix counter.
def load_prefix_counter(file_path="prefix_counter.json"):
    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        try:
            with open(file_path, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            logging.warning(f"Corrupted JSON in {file_path}, returning empty prefix counter.")
            return {}
    return {}

