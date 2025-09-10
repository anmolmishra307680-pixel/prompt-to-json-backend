import re

def extract_basic_fields(prompt):
    """Extract structured info from text using enhanced pattern matching."""
    prompt_lower = prompt.lower()
    
    # Enhanced type extraction with more patterns
    type_patterns = {
        'table': ['table', 'desk', 'surface'],
        'chair': ['chair', 'seat', 'stool'],
        'shelf': ['shelf', 'shelving', 'bookcase'],
        'cabinet': ['cabinet', 'cupboard', 'storage'],
        'sofa': ['sofa', 'couch', 'settee'],
        'bed': ['bed', 'mattress'],
        'drone': ['drone', 'aircraft', 'uav'],
        'library': ['library', 'building'],
        'throne': ['throne', 'chair']
    }
    
    type_match = None
    for main_type, patterns in type_patterns.items():
        if any(pattern in prompt_lower for pattern in patterns):
            type_match = main_type
            break
    
    # Enhanced material extraction
    material_patterns = {
        'wood': ['wood', 'wooden', 'oak', 'pine', 'mahogany'],
        'metal': ['metal', 'steel', 'aluminum', 'iron'],
        'glass': ['glass', 'crystal'],
        'plastic': ['plastic', 'polymer'],
        'fabric': ['fabric', 'cloth', 'textile'],
        'leather': ['leather', 'hide'],
        'concrete': ['concrete', 'cement'],
        'carbon fiber': ['carbon fiber', 'carbon fibre', 'composite']
    }
    
    material_match = None
    for material, patterns in material_patterns.items():
        if any(pattern in prompt_lower for pattern in patterns):
            material_match = material
            break
    
    # Enhanced color extraction
    color_patterns = ['red', 'blue', 'green', 'black', 'white', 'brown', 'gray', 'grey', 'yellow', 'gold', 'silver']
    color_match = next((c for c in color_patterns if c in prompt_lower), None)
    
    # Enhanced dimension extraction
    dimension_pattern = r'(\d+(?:\.\d+)?)\s*(?:x\s*(\d+(?:\.\d+)?))?\s*(feet|ft|cm|m|inches|in|floor)'
    dimensions = re.findall(dimension_pattern, prompt_lower)
    dimension_str = ', '.join([f"{d[0]}{f'x{d[1]}' if d[1] else ''} {d[2]}" for d in dimensions]) if dimensions else None
    
    # Enhanced purpose extraction
    purpose_patterns = {
        'dining': ['dining', 'eat'],
        'office': ['office', 'work', 'desk'],
        'bedroom': ['bedroom', 'sleep'],
        'living room': ['living room', 'lounge'],
        'kitchen': ['kitchen', 'cook'],
        'storage': ['storage', 'organize'],
        'library': ['library', 'book', 'read'],
        'medical': ['medical', 'surgical', 'hospital']
    }
    
    purpose_match = None
    for purpose, patterns in purpose_patterns.items():
        if any(pattern in prompt_lower for pattern in patterns):
            purpose_match = purpose
            break
    
    # Return structured dictionary with extracted fields
    return {
        'type': type_match,
        'material': material_match,
        'color': color_match,
        'dimensions': dimension_str,
        'purpose': purpose_match
    }

# Test with sample prompts
if __name__ == "__main__":
    test_prompts = [
        "Create a wooden dining table that is 6 feet long and brown in color",
        "I need a black metal office chair for my workspace",
        "Design a white plastic storage shelf 5x3 feet for the kitchen",
        "Make a red fabric sofa for the living room"
    ]
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"Prompt {i}: {prompt}")
        result = extract_basic_fields(prompt)
        print(f"Extracted: {result}")
        print("-" * 50)