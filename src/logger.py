import json
import os
from datetime import datetime

def append_log(prompt, output, log_file="logs.json"):
    """Append timestamped log entry to logs.json."""
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "prompt": prompt,
        "output": output
    }
    
    if os.path.exists(log_file):
        with open(log_file, 'r') as f:
            logs = json.load(f)
    else:
        logs = []
    
    logs.append(log_entry)
    
    with open(log_file, 'w') as f:
        json.dump(logs, f, indent=2)

def get_last_prompts(n, log_file="logs.json"):
    """Get last n prompts from logs.json."""
    if not os.path.exists(log_file):
        return []
    
    with open(log_file, 'r') as f:
        logs = json.load(f)
    
    return logs[-n:] if len(logs) >= n else logs

if __name__ == "__main__":
    # Test logging system
    test_entries = [
        ("Create a modern chair", "Generated chair design with sleek lines"),
        ("Design a wooden desk", "Created desk specification with oak material")
    ]
    
    for prompt, output in test_entries:
        append_log(prompt, output)
        print(f"Logged: {prompt}")
    
    # Test retrieval
    last_2 = get_last_prompts(2)
    print(f"\nLast 2 prompts:")
    for entry in last_2:
        print(f"- {entry['timestamp']}: {entry['prompt']}")