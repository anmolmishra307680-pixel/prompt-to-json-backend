import json
import os

def append_log(entry: dict):
    """Append a log entry to data/logs.json in JSONL format"""
    log_file = "data/logs.json"
    
    # Read existing logs
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            try:
                logs = json.load(f)
            except json.JSONDecodeError:
                logs = []
    else:
        logs = []
    
    # Append new entry
    logs.append(entry)
    
    # Write back to file
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)