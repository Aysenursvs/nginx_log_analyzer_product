import json
import os

def save_ip_data_to_file(file_path, ip_datas):
    try:
        with open(file_path, 'w') as f:
            json.dump(ip_datas, f, default=str, indent=4)
    except Exception as e:
        print(f"Error while saving data: {e}")

def save_single_ip_data(file_path, ip, ip_data):
    # Dosya varsa oku, yoksa boş dict başlat
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            try:
                data = json.load(f)
            except json.JSONDecodeError:
                data = {}
    else:
        data = {}

    # IP verisini güncelle
    data[ip] = ip_data

    # Dosyaya tekrar yaz
    with open(file_path, 'w') as f:
        json.dump(data, f, default=str, indent=4)

def save_bad_lines_to_file(bad_lines):
    """
    Saves bad log lines to a file for later review.
    
    :param bad_lines: List of bad log lines
    """
    if not bad_lines:
        return
    
    with open("bad_log_lines.txt", "w") as f:
        for line_number, line_content in bad_lines:
            f.write(f"[Line {line_number}]: {line_content}")

def save_ip_location_cache(cache, file_path="ip_location_cache.json"):
    with open(file_path, "w") as f:
        json.dump(cache, f, indent=4)

def save_prefix_counter(counter, file_path="prefix_counter.json"):
    with open(file_path, "w") as f:
        json.dump(counter, f, indent=4)