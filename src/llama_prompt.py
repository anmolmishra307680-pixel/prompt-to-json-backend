from transformers import pipeline
import json
import os
from datetime import datetime

def load_model():
    """Load HuggingFace pipeline with DistilGPT2."""
    return pipeline("text-generation", model="distilgpt2", max_length=100)

def generate_response(prompt, generator):
    """Generate response from model."""
    response = generator(prompt, max_new_tokens=50, do_sample=True, temperature=0.7)
    return response[0]['generated_text']

def save_log(prompt, output, log_file="logs.json"):
    """Save prompt and output to logs.json."""
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

if __name__ == "__main__":
    generator = load_model()
    
    test_prompts = [
        "Create a wooden dining table",
        "Design a metal office chair",
        "Make a storage shelf for kitchen"
    ]
    
    for prompt in test_prompts:
        print(f"Processing: {prompt}")
        output = generate_response(prompt, generator)
        save_log(prompt, output)
        print(f"Generated: {output}")
        print("-" * 50)