"""Unified utility functions for the prompt-to-json system."""

def apply_fallbacks(extracted_fields):
    """Apply consistent fallback values for missing fields."""
    return {
        'type': extracted_fields.get('type') or 'unknown',
        'material': extracted_fields.get('material') or 'unspecified',
        'color': extracted_fields.get('color') or 'default',
        'dimensions': extracted_fields.get('dimensions') or 'standard',
        'purpose': extracted_fields.get('purpose') or 'general'
    }

def save_json(data, filepath):
    """Save data to JSON file with proper formatting."""
    import json
    import os
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    return filepath