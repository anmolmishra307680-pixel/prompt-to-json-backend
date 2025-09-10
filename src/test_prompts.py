from extractor import extract_basic_fields
from schema import validate_and_save
from logger import append_log

def process_prompt(prompt, filename):
    """Process prompt through extraction, validation, and logging."""
    # Extract fields with fallback values
    extracted = extract_basic_fields(prompt)
    
    # Add fallback values for missing fields
    fallback_data = {
        'type': extracted.get('type') or 'unknown',
        'material': extracted.get('material') or 'unspecified',
        'color': extracted.get('color') or 'default',
        'dimensions': extracted.get('dimensions') or 'standard',
        'purpose': extracted.get('purpose') or 'general'
    }
    
    # Validate and save
    spec = validate_and_save(fallback_data, filename)
    
    # Log the process
    append_log(prompt, f"Generated spec: {spec.dict()}")
    
    return spec

if __name__ == "__main__":
    test_prompts = [
        ("Create a blue leather sofa for living room", "blue_sofa_spec.json"),
        ("I want a glass desk", "glass_desk_spec.json"),
        ("Make a 4x2 feet metal shelf", "metal_shelf_spec.json"),
        ("Design bedroom furniture", "bedroom_furniture_spec.json"),
        ("Build a red wooden cabinet 3 feet tall", "red_cabinet_spec.json")
    ]
    
    print("Processing 5 test prompts...")
    for prompt, filename in test_prompts:
        print(f"\nProcessing: {prompt}")
        spec = process_prompt(prompt, filename)
        print(f"Generated: {filename}")
        print(f"Spec: {spec.dict()}")
    
    print(f"\nCompleted! Generated {len(test_prompts)} JSON files in spec_outputs/")