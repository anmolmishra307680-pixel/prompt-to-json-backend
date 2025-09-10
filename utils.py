"""Unified utility functions for the prompt-to-json system."""

def apply_fallbacks(extracted_fields):
    """Apply consistent fallback values for missing fields with smart defaults."""
    # Smart purpose fallback based on type
    purpose = extracted_fields.get('purpose')
    if not purpose:
        type_val = extracted_fields.get('type')
        smart_purpose_map = {
            'drone': 'aerial',
            'throne': 'ceremonial', 
            'library': 'library',
            'cabinet': 'storage',
            'table': 'dining',
            'chair': 'office'
        }
        purpose = smart_purpose_map.get(type_val, 'general')
    
    return {
        'type': extracted_fields.get('type') or 'unknown',
        'material': extracted_fields.get('material') or 'unspecified',
        'color': extracted_fields.get('color') or 'default',
        'dimensions': extracted_fields.get('dimensions') or 'standard',
        'purpose': purpose
    }

def save_json(data, filepath):
    """Save data to JSON file with proper formatting."""
    import json
    import os
    
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)
    return filepath