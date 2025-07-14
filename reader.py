
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

