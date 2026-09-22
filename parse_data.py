import json
import os

def load_items(filename):
    with open(filename, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def get_unclaimed_items(data):
    unclaimed = []
    for item in data["items"]:
        if item["status"] == "unclaimed":
            unclaimed.append(item)
    return unclaimed

def save_result(data, out_path):
    folder = os.path.dirname(out_path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)
