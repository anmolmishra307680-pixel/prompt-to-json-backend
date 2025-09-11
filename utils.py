"""Utility functions for prompt-to-json agent."""

import json
import os

def apply_fallbacks(extracted_data):
    """Apply smart fallbacks for missing fields."""
    # Set defaults for missing fields
    if not extracted_data.get('type'):
        extracted_data['type'] = 'unknown'
    
    if not extracted_data.get('material'):
        extracted_data['material'] = ['unspecified']
    elif isinstance(extracted_data['material'], str):
        extracted_data['material'] = [extracted_data['material']]
    
    if not extracted_data.get('color'):
        extracted_data['color'] = 'default'
    
    if not extracted_data.get('purpose'):
        extracted_data['purpose'] = 'general'
    
    return extracted_data

def save_json(data, filepath):
    """Save data as JSON file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)