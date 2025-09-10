"""Unified utility functions for the prompt-to-json system."""

def apply_fallbacks(extracted_fields):
    """Apply consistent fallback values with context-aware smart defaults."""
    # Smart purpose fallback based on type
    purpose = extracted_fields.get('purpose')
    if not purpose:
        type_val = extracted_fields.get('type')
        smart_purpose_map = {
            'drone': 'aerial',
            'throne': 'ceremonial', 
            'library': 'study',
            'cabinet': 'storage',
            'table': 'dining',
            'chair': 'seating',
            'shelf': 'storage',
            'sofa': 'seating',
            'bed': 'sleeping'
        }
        purpose = smart_purpose_map.get(type_val, 'general')
    
    # Smart color defaults based on material/type
    color = extracted_fields.get('color')
    if not color:
        material = extracted_fields.get('material') or ''
        type_val = extracted_fields.get('type')
        
        if material and 'wood' in str(material).lower():
            color = 'brown'
        elif material and ('metal' in str(material).lower() or 'steel' in str(material).lower()):
            color = 'silver'
        elif type_val == 'throne':
            color = 'gold'
        else:
            color = 'default'
    
    # Smart dimension defaults with units
    dimensions = extracted_fields.get('dimensions')
    if not dimensions:
        type_val = extracted_fields.get('type')
        smart_dimension_map = {
            'table': '4x2 feet',
            'chair': '2x2 feet', 
            'cabinet': '3x2 feet',
            'shelf': '4x1 feet',
            'drone': '1x1 feet',
            'throne': '3x3 feet'
        }
        dimensions = smart_dimension_map.get(type_val, 'standard')
    
    return {
        'type': extracted_fields.get('type') or 'unknown',
        'material': extracted_fields.get('material') or 'unspecified',
        'color': color,
        'dimensions': dimensions,
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