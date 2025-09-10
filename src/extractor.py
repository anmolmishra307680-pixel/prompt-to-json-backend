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
    
    # Enhanced multi-material extraction
    material_patterns = {
        'wood': ['wood', 'wooden', 'oak', 'pine', 'mahogany'],
        'metal': ['metal', 'steel', 'aluminum', 'iron', 'stainless steel'],
        'glass': ['glass', 'crystal'],
        'plastic': ['plastic', 'polymer'],
        'fabric': ['fabric', 'cloth', 'textile'],
        'leather': ['leather', 'hide'],
        'concrete': ['concrete', 'cement'],
        'carbon fiber': ['carbon fiber', 'carbon fibre', 'composite']
    }
    
    # Find all matching materials
    material_matches = []
    for material, patterns in material_patterns.items():
        if any(pattern in prompt_lower for pattern in patterns):
            material_matches.append(material)
    
    # Return primary material or combined materials
    if len(material_matches) > 1:
        material_match = ', '.join(material_matches)
    elif material_matches:
        material_match = material_matches[0]
    else:
        material_match = None
    
    # Enhanced color extraction
    color_patterns = ['red', 'blue', 'green', 'black', 'white', 'brown', 'gray', 'grey', 'yellow', 'gold', 'silver']
    color_match = next((c for c in color_patterns if c in prompt_lower), None)
    
    # Enhanced dimension extraction with descriptive terms
    dimension_patterns = [
        r'(\d+(?:\.\d+)?)\s*(?:x\s*(\d+(?:\.\d+)?))?\s*(feet|ft|cm|m|inches|in)',
        r'(\d+)[-\s]*floor',
        r'(small|medium|large|compact|lightweight|massive)'
    ]
    
    dimension_matches = []
    for pattern in dimension_patterns:
        matches = re.findall(pattern, prompt_lower)
        if matches:
            if isinstance(matches[0], tuple):
                dimension_matches.extend([' '.join(filter(None, match)) for match in matches])
            else:
                dimension_matches.extend(matches)
    
    dimension_str = ', '.join(dimension_matches) if dimension_matches else None
    
    # Enhanced purpose extraction with type-aware context
    purpose_patterns = {
        'dining': ['dining', 'eat', 'meal'],
        'office': ['office', 'work', 'workspace'],
        'bedroom': ['bedroom', 'sleep', 'rest'],
        'living room': ['living room', 'lounge', 'family room'],
        'kitchen': ['kitchen', 'cook', 'culinary'],
        'storage': ['storage', 'organize'],
        'library': ['library', 'book', 'read', 'study'],
        'medical': ['medical', 'surgical', 'hospital', 'clinic'],
        'aerial': ['aerial', 'photography', 'cinematography', 'flying'],
        'ceremonial': ['medieval', 'throne', 'royal', 'ceremonial']
    }
    
    # Find purpose with type context awareness
    purpose_match = None
    for purpose, patterns in purpose_patterns.items():
        if any(pattern in prompt_lower for pattern in patterns):
            purpose_match = purpose
            break
    
    # Type-specific purpose inference
    if not purpose_match and type_match:
        type_purpose_map = {
            'drone': 'aerial',
            'throne': 'ceremonial',
            'library': 'library',
            'cabinet': 'storage'
        }
        purpose_match = type_purpose_map.get(type_match)
    
    # Return structured dictionary with extracted fields
    return {
        'type': type_match,
        'material': material_match,
        'color': color_match,
        'dimensions': dimension_str,
        'purpose': purpose_match
    }

# Enhanced test with complex prompts
if __name__ == "__main__":
    test_prompts = [
        "Create a wooden dining table that is 6 feet long and brown in color",
        "Design a lightweight carbon fiber drone body for aerial photography",
        "Build a 2-floor eco-friendly library with glass walls",
        "Make a compact steel surgical instrument cabinet for hospital use",
        "Create a medieval wooden throne with gold accents"
    ]
    
    print("Enhanced Extraction Test Results:")
    print("=" * 60)
    
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\nPrompt {i}: {prompt}")
        result = extract_basic_fields(prompt)
        print(f"Extracted: {result}")
        
        # Show extraction success rate
        filled_fields = sum(1 for v in result.values() if v is not None)
        print(f"Fields extracted: {filled_fields}/5 ({filled_fields*20}% complete)")
        print("-" * 50)