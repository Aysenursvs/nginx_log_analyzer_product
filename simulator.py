import time
def simulate_logging(source_file, target_file):
    with open(source_file, "r") as source, open(target_file, "a") as target:
        for line in source:
            target.write(line)
            target.flush()
            #time.sleep(0.5)