import re
from evaluator_agent import KNOWN_MATERIALS

def parse_dimensions(dimensions_str):
    """Parse dimension string into normalized dictionary."""
    if not dimensions_str or dimensions_str in ['standard', 'default']:
        return {}
    
    dimensions_str = dimensions_str.lower()
    parsed = {}
    
    # Parse floor count
    floor_match = re.search(r'(\d+)[-\s]*floor', dimensions_str)
    if floor_match:
        parsed['floors'] = int(floor_match.group(1))
    
    # Parse area (sqm, sq ft, etc.)
    area_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:sq\s*)?m', dimensions_str)
    if area_match:
        parsed['area_m2'] = float(area_match.group(1))
    
    # Parse dimensions like 15x20m, 6x4 feet
    dim_match = re.search(r'(\d+(?:\.\d+)?)\s*x\s*(\d+(?:\.\d+)?)\s*(m|feet|ft)', dimensions_str)
    if dim_match:
        length, width, unit = dim_match.groups()
        if unit in ['feet', 'ft']:
            # Convert to meters
            parsed['length_m'] = float(length) * 0.3048
            parsed['width_m'] = float(width) * 0.3048
        else:
            parsed['length_m'] = float(length)
            parsed['width_m'] = float(width)
    
    # Parse single dimension
    single_match = re.search(r'(\d+(?:\.\d+)?)\s*(feet|ft|m|cm)', dimensions_str)
    if single_match and not dim_match:
        value, unit = single_match.groups()
        if unit in ['feet', 'ft']:
            parsed['size_m'] = float(value) * 0.3048
        elif unit == 'cm':
            parsed['size_m'] = float(value) / 100
        else:
            parsed['size_m'] = float(value)
    
    return parsed

def score_spec(spec, prompt):
    """Score spec for completeness, realism, and format (0-10)."""
    explanations = []
    
    # Completeness score (0-4)
    completeness_score = 0
    required_fields = ['type', 'material', 'dimensions', 'purpose']
    for field in required_fields:
        value = spec.get(field, '')
        if value and value not in ['unknown', 'unspecified', 'default', 'standard', 'general']:
            completeness_score += 1
        else:
            explanations.append(f"Missing or default value for {field}")
    
    # Material realism score (0-3)
    material_realism_score = 0
    material = spec.get('material', '').lower()
    if material in [m.lower() for m in KNOWN_MATERIALS]:
        material_realism_score = 3
    elif material and material not in ['unspecified', 'default']:
        material_realism_score = 1
        explanations.append(f"Material '{material}' not in known materials list")
    else:
        explanations.append("No material specified")
    
    # Dimension validity score (0-2)
    dimension_validity_score = 0
    dimensions = spec.get('dimensions', '')
    parsed_dims = parse_dimensions(dimensions)
    
    if parsed_dims:
        dimension_validity_score = 1
        # Check for reasonable ranges
        reasonable = True
        for key, value in parsed_dims.items():
            if 'floor' in key and (value < 1 or value > 50):
                reasonable = False
            elif 'area' in key and (value < 0.1 or value > 10000):
                reasonable = False
            elif 'length' in key or 'width' in key or 'size' in key:
                if value < 0.1 or value > 100:
                    reasonable = False
        
        if reasonable:
            dimension_validity_score = 2
        else:
            explanations.append("Dimensions outside reasonable ranges")
    else:
        explanations.append("Dimensions not parseable or missing")
    
    # Type match score (0-1)
    type_match_score = 0
    spec_type = spec.get('type', '').lower()
    prompt_lower = prompt.lower()
    
    furniture_types = ['table', 'chair', 'desk', 'shelf', 'cabinet', 'sofa', 'bed', 'drone']
    for ftype in furniture_types:
        if ftype in prompt_lower and ftype in spec_type:
            type_match_score = 1
            break
    
    if type_match_score == 0 and spec_type not in ['unknown', '']:
        explanations.append(f"Type '{spec_type}' doesn't match prompt context")
    
    # Calculate format score (0-10)
    max_score = 4 + 3 + 2 + 1  # 10 total
    total_score = completeness_score + material_realism_score + dimension_validity_score + type_match_score
    format_score = (total_score / max_score) * 10
    
    return {
        "format_score": round(format_score, 1),
        "completeness_score": completeness_score,
        "material_realism_score": material_realism_score,
        "dimension_validity_score": dimension_validity_score,
        "type_match_score": type_match_score,
        "explanations": explanations
    }

def create_dashboard(prompt, spec, evaluator_result, reward):
    """Create combined dashboard with spec score, critic, and reward."""
    score_result = score_spec(spec, prompt)
    
    return {
        "prompt": prompt,
        "spec_score": score_result["format_score"],
        "completeness_score": score_result["completeness_score"],
        "material_realism_score": score_result["material_realism_score"],
        "dimension_validity_score": score_result["dimension_validity_score"],
        "type_match_score": score_result["type_match_score"],
        "critic": evaluator_result.get("critic_feedback", ""),
        "reward": reward,
        "explanations": score_result["explanations"]
    }

if __name__ == "__main__":
    # Test scoring
    test_spec = {
        "type": "table",
        "material": "wood",
        "color": "brown",
        "dimensions": "6x4 feet",
        "purpose": "dining"
    }
    
    result = score_spec(test_spec, "Create a wooden dining table")
    print("Test scoring result:")
    print(f"Format score: {result['format_score']}")
    print(f"Completeness: {result['completeness_score']}/4")
    print(f"Material realism: {result['material_realism_score']}/3")
    print(f"Dimension validity: {result['dimension_validity_score']}/2")
    print(f"Type match: {result['type_match_score']}/1")
    print(f"Explanations: {result['explanations']}")