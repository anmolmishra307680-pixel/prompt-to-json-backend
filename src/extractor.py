import re

# Known materials for extraction
KNOWN_MATERIALS = [
    'wood', 'wooden', 'oak', 'pine', 'mahogany',
    'metal', 'steel', 'aluminum', 'iron', 'stainless steel',
    'glass', 'crystal',
    'plastic', 'polymer',
    'fabric', 'cloth', 'textile',
    'leather', 'hide',
    'concrete', 'cement',
    'carbon fiber', 'carbon fibre', 'composite'
]

def extract_basic_fields(prompt):
    """Extract structured info with improved regex parsing."""
    prompt_lower = prompt.lower()
    
    # Type extraction
    type_patterns = {
        'building': ['library', 'building', 'structure'],
        'table': ['table', 'desk', 'surface'],
        'chair': ['chair', 'seat', 'stool', 'throne'],
        'shelf': ['shelf', 'shelving', 'bookcase'],
        'cabinet': ['cabinet', 'cupboard'],
        'sofa': ['sofa', 'couch'],
        'bed': ['bed', 'mattress'],
        'drone': ['drone', 'aircraft', 'uav']
    }
    
    type_match = None
    for main_type, patterns in type_patterns.items():
        if any(pattern in prompt_lower for pattern in patterns):
            type_match = main_type
            break
    
    # Material extraction using known materials list
    material_matches = []
    for material in KNOWN_MATERIALS:
        if material in prompt_lower:
            # Map specific materials to categories
            if material in ['wood', 'wooden', 'oak', 'pine', 'mahogany']:
                if 'wood' not in material_matches:
                    material_matches.append('wood')
            elif material in ['metal', 'steel', 'aluminum', 'iron', 'stainless steel']:
                if 'metal' not in material_matches:
                    material_matches.append('metal')
            elif material in ['glass', 'crystal']:
                if 'glass' not in material_matches:
                    material_matches.append('glass')
            elif material in ['concrete', 'cement']:
                if 'concrete' not in material_matches:
                    material_matches.append('concrete')
            elif material in ['carbon fiber', 'carbon fibre', 'composite']:
                if 'carbon fiber' not in material_matches:
                    material_matches.append('carbon fiber')
            else:
                if material not in material_matches:
                    material_matches.append(material)
    
    # Color extraction
    color_patterns = ['red', 'blue', 'green', 'black', 'white', 'brown', 'gray', 'grey', 'yellow', 'gold', 'silver']
    color_match = next((c for c in color_patterns if c in prompt_lower), None)
    if color_match == 'grey':
        color_match = 'gray'  # Normalize spelling
    
    # Enhanced dimension parsing with regex
    dimensions = parse_dimensions(prompt_lower)
    
    # Purpose extraction
    purpose_patterns = {
        'library': ['library', 'study', 'reading'],
        'dining': ['dining', 'eat', 'meal'],
        'office': ['office', 'work'],
        'storage': ['storage', 'organize'],
        'medical': ['medical', 'surgical', 'hospital'],
        'aerial': ['aerial', 'photography', 'flying']
    }
    
    purpose_match = None
    for purpose, patterns in purpose_patterns.items():
        if any(pattern in prompt_lower for pattern in patterns):
            purpose_match = purpose
            break
    
    return {
        'type': type_match,
        'material': material_matches,
        'color': color_match if color_match else 'none',
        'dimensions': dimensions,
        'purpose': purpose_match
    }

def parse_dimensions(text):
    """Parse dimensions using regex patterns."""
    result = {
        'floors': None,
        'area_m2': None,
        'raw': None
    }
    
    # Floor count: (\d+)[ -]?floor(s)?
    floor_pattern = r'(\d+)[ -]?floors?'
    floor_match = re.search(floor_pattern, text)
    if floor_match:
        result['floors'] = int(floor_match.group(1))
        result['raw'] = floor_match.group(0)
    
    # Dimensions: (\d+(\.\d+)?)(\s?(m|cm|mm|sqm|sqft))
    dim_pattern = r'(\d+(?:\.\d+)?)\s?(m|cm|mm|sqm|sqft|feet|ft)'
    dim_matches = re.findall(dim_pattern, text)
    
    if dim_matches:
        for value, unit in dim_matches:
            if unit in ['sqm', 'sq m']:
                result['area_m2'] = float(value)
            elif unit in ['sqft', 'sq ft']:
                result['area_m2'] = float(value) * 0.092903  # Convert sqft to sqm
        
        if not result['raw']:
            result['raw'] = f"{dim_matches[0][0]} {dim_matches[0][1]}"
    
    return result

# Test with improved parsing
if __name__ == "__main__":
    test_prompts = [
        "Design a 2-floor library using glass and concrete",
        "Create a wooden dining table 6 feet long",
        "Build a steel cabinet for medical storage",
        "Make a 50 sqm office with aluminum frame",
        "Design a 3-floor building with glass walls"
    ]
    
    print("Improved Extraction Test Results:")
    print("=" * 60)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nPrompt {i}: {prompt}")
        result = extract_basic_fields(prompt)
        print(f"Extracted: {result}")
        print("-" * 50)