import time

# This function simulates logging by reading from a source file and writing to a target file.
# It reads each line from the source file and writes it to the target file.
# It is used in the main.py file to simulate logging while processing the log lines.
# The target file is dynamic, meaning new log lines are added to it.
# The source file is static, meaning new log lines are not added to it.
# The function can be run in a separate thread to simulate real-time logging.
def simulate_logging(source_file, target_file):
    with open(source_file, "r") as source, open(target_file, "a") as target:
        for line in source:
            target.write(line)
            target.flush()
            #time.sleep(0.5)