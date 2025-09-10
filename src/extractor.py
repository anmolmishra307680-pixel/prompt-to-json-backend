import re

def extract_basic_fields(prompt):
    """Extract structured info from text using simple pattern matching rules."""
    prompt_lower = prompt.lower()
    
    # Extract furniture type using predefined patterns
    type_patterns = ['table', 'chair', 'desk', 'shelf', 'cabinet', 'sofa', 'bed']
    type_match = next((t for t in type_patterns if t in prompt_lower), None)
    
    # Extract material using common furniture materials
    material_patterns = ['wood', 'metal', 'plastic', 'glass', 'fabric', 'leather']
    material_match = next((m for m in material_patterns if m in prompt_lower), None)
    
    # Extract color using basic color names
    color_patterns = ['red', 'blue', 'green', 'black', 'white', 'brown', 'gray', 'yellow']
    color_match = next((c for c in color_patterns if c in prompt_lower), None)
    
    # Extract dimensions using regex for measurements (e.g., "5 feet", "10cm", "2x3")
    dimension_pattern = r'(\d+(?:\.\d+)?)\s*(?:x\s*(\d+(?:\.\d+)?))?\s*(feet|ft|cm|m|inches|in)'
    dimensions = re.findall(dimension_pattern, prompt_lower)
    dimension_str = ', '.join([f"{d[0]}{f'x{d[1]}' if d[1] else ''} {d[2]}" for d in dimensions]) if dimensions else None
    
    # Extract purpose/room context
    purpose_patterns = ['dining', 'office', 'bedroom', 'living room', 'kitchen', 'storage', 'work']
    purpose_match = next((p for p in purpose_patterns if p in prompt_lower), None)
    
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