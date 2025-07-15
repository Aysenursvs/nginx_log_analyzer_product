import json

def save_ip_data_to_file(file_path, ip_datas):
    try:
        with open(file_path, 'w') as f:
            json.dump(ip_datas, f, default=str, indent=4)
    except Exception as e:
        print(f"Error while saving data: {e}")
