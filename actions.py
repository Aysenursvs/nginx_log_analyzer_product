def give_warning(ip_data:dict, ip):
    if ip_data["action"] != "normal":
        if ip_data['action'] == "review" and not ip_data["review_warning"]:
            print(f"Review Warning: IP {ip} has action '{ip_data['action']}' with risk score {ip_data['risk_score']}.")
            ip_data["review_warning"] = True
        if ip_data['action'] == "block" and not ip_data["block_warning"]:
            print(f"Block Warning: IP {ip} has action '{ip_data['action']}' with risk score {ip_data['risk_score']}.")
            ip_data["block_warning"] = True
