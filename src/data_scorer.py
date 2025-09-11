"""Data quality scoring module for design specifications."""

import re
from typing import Dict, List, Any, Tuple

# Known materials for validation
KNOWN_MATERIALS = [
    "wood", "wooden", "oak", "pine", "mahogany", "cedar", "birch", "maple",
    "metal", "steel", "aluminum", "iron", "copper", "brass", "stainless steel", "titanium",
    "glass", "crystal", "tempered glass", "laminated glass",
    "plastic", "polymer", "acrylic", "polycarbonate", "PVC",
    "fabric", "cloth", "textile", "cotton", "linen", "silk", "wool",
    "leather", "hide", "suede", "faux leather",
    "concrete", "cement", "reinforced concrete",
    "carbon fiber", "carbon fibre", "fiberglass", "composite",
    "marble", "granite", "limestone", "sandstone", "slate",
    "ceramic", "porcelain", "tile", "clay"
]

# Valid object types
VALID_TYPES = [
    "table", "chair", "sofa", "bed", "desk", "shelf", "cabinet", "stool",
    "building", "house", "library", "office", "warehouse", "garage",
    "drone", "robot", "vehicle", "machine", "tool", "instrument"
]

def score_completeness(spec: Dict[str, Any]) -> Tuple[int, List[str]]:
    """Score completeness (0-4) based on required fields."""
    score = 0
    explanations = []
    
    # Type (1 point)
    if spec.get('type') and spec['type'] not in ['unknown', 'unspecified', None]:
        score += 1
        explanations.append("type specified")
    else:
        explanations.append("type missing")
    
    # Material (1 point)
    material = spec.get('material', [])
    if isinstance(material, str):
        material = [material]
    
    if material and any(m.strip() for m in material if m not in ['unspecified', 'default', 'none']):
        score += 1
        explanations.append("material specified")
    else:
        explanations.append("material missing")
    
    # Dimensions (1 point)
    dimensions = spec.get('dimensions')
    has_dimensions = False
    
    if isinstance(dimensions, dict):
        if dimensions.get('floors') or dimensions.get('area_m2') or (dimensions.get('raw') and dimensions['raw'] not in ['None', '', None]):
            has_dimensions = True
    elif isinstance(dimensions, str) and dimensions not in ['standard', 'default', 'None', '', None]:
        has_dimensions = True
    
    if has_dimensions:
        score += 1
        explanations.append("dimensions provided")
    else:
        explanations.append("dimensions missing")
    
    # Purpose (1 point)
    if spec.get('purpose') and spec['purpose'] not in ['general', 'unspecified', None]:
        score += 1
        explanations.append("purpose specified")
    else:
        explanations.append("purpose missing")
    
    return score, explanations

def score_material_realism(spec: Dict[str, Any]) -> Tuple[int, List[str]]:
    """Score material realism (0-3) based on material validity."""
    score = 0
    explanations = []
    
    material = spec.get('material', [])
    if isinstance(material, str):
        material = [material]
    
    if not material or not any(m.strip() for m in material):
        explanations.append("no materials specified")
        return 0, explanations
    
    # Check if materials are recognized (1 point)
    recognized_materials = []
    unrecognized_materials = []
    
    for mat in material:
        mat_clean = mat.lower().strip()
        if mat_clean in ['none', 'default', 'unspecified']:
            continue
            
        if any(known.lower() == mat_clean or mat_clean in known.lower() for known in KNOWN_MATERIALS):
            recognized_materials.append(mat)
        else:
            unrecognized_materials.append(mat)
    
    if recognized_materials and not unrecognized_materials:
        score += 1
        explanations.append("all materials recognized")
    elif recognized_materials:
        score += 0.5
        explanations.append(f"some materials unrecognized: {', '.join(unrecognized_materials)}")
    else:
        explanations.append("materials not recognized")
    
    # Check material count appropriateness (1 point)
    if len(recognized_materials) == 1:
        score += 1
        explanations.append("single material appropriate")
    elif 2 <= len(recognized_materials) <= 3:
        score += 1
        explanations.append("multi-material combination reasonable")
    elif len(recognized_materials) > 3:
        score += 0.5
        explanations.append("many materials specified (may be complex)")
    
    # Check material-type compatibility (1 point)
    spec_type = spec.get('type', '').lower()
    if spec_type and recognized_materials:
        compatible = check_material_type_compatibility(spec_type, recognized_materials)
        if compatible:
            score += 1
            explanations.append("materials compatible with type")
        else:
            explanations.append("materials may not be suitable for type")
    
    return min(int(score), 3), explanations

def score_dimension_validity(spec: Dict[str, Any]) -> Tuple[int, List[str]]:
    """Score dimension validity (0-2) based on format and reasonableness."""
    score = 0
    explanations = []
    
    dimensions = spec.get('dimensions')
    
    if not dimensions:
        explanations.append("no dimensions provided")
        return 0, explanations
    
    # Check format and units (1 point)
    has_units = False
    has_numeric = False
    
    if isinstance(dimensions, dict):
        raw = dimensions.get('raw', '')
        floors = dimensions.get('floors')
        area_m2 = dimensions.get('area_m2')
        
        if floors and isinstance(floors, (int, float)):
            has_numeric = True
            has_units = True  # floors are inherently unit-ed
        
        if area_m2 and isinstance(area_m2, (int, float)):
            has_numeric = True
            has_units = True  # area has implicit units
        
        if raw and isinstance(raw, str):
            if any(unit in raw.lower() for unit in ['feet', 'ft', 'cm', 'm', 'inches', 'in', 'floor']):
                has_units = True
            if re.search(r'\d+', raw):
                has_numeric = True
    
    elif isinstance(dimensions, str):
        if any(unit in dimensions.lower() for unit in ['feet', 'ft', 'cm', 'm', 'inches', 'in', 'floor']):
            has_units = True
        if re.search(r'\d+', dimensions):
            has_numeric = True
    
    if has_units and has_numeric:
        score += 1
        explanations.append("dimensions have units and numeric values")
    elif has_numeric:
        score += 0.5
        explanations.append("dimensions have numeric values but unclear units")
    else:
        explanations.append("dimensions lack numeric values or units")
    
    # Check reasonableness (1 point)
    reasonable = True
    if isinstance(dimensions, dict):
        floors = dimensions.get('floors')
        area_m2 = dimensions.get('area_m2')
        
        if floors and (floors < 1 or floors > 50):
            reasonable = False
            explanations.append(f"floor count ({floors}) unreasonable")
        
        if area_m2 and (area_m2 < 0.1 or area_m2 > 10000):
            reasonable = False
            explanations.append(f"area ({area_m2} m²) unreasonable")
    
    if reasonable:
        score += 1
        explanations.append("dimensions appear reasonable")
    
    return min(score, 2), explanations

def score_type_match(spec: Dict[str, Any], prompt: str) -> Tuple[int, List[str]]:
    """Score type match (0-1) based on prompt-spec consistency."""
    score = 0
    explanations = []
    
    spec_type = (spec.get('type') or '').lower()
    prompt_lower = prompt.lower()
    
    if not spec_type or spec_type in ['unknown', 'unspecified']:
        explanations.append("no type specified")
        return 0, explanations
    
    # Check if type appears in prompt or is implied
    type_keywords = {
        'table': ['table', 'desk', 'surface'],
        'chair': ['chair', 'seat', 'stool'],
        'building': ['building', 'library', 'house', 'structure'],
        'cabinet': ['cabinet', 'cupboard', 'storage'],
        'shelf': ['shelf', 'shelving', 'bookcase'],
        'drone': ['drone', 'aircraft', 'uav'],
        'sofa': ['sofa', 'couch'],
        'bed': ['bed', 'mattress']
    }
    
    keywords = type_keywords.get(spec_type, [spec_type])
    
    if any(keyword in prompt_lower for keyword in keywords):
        score = 1
        explanations.append("type matches prompt")
    else:
        explanations.append("type may not match prompt intent")
    
    return score, explanations

def calculate_format_score(spec: Dict[str, Any]) -> Tuple[float, List[str]]:
    """Calculate overall format score (0-10) based on all components."""
    explanations = []
    
    # Get individual scores
    completeness, comp_exp = score_completeness(spec)
    material_realism, mat_exp = score_material_realism(spec)
    dimension_validity, dim_exp = score_dimension_validity(spec)
    
    # Combine explanations
    explanations.extend(comp_exp)
    explanations.extend(mat_exp)
    explanations.extend(dim_exp)
    
    # Calculate weighted score (out of 10)
    # Completeness: 4 points, Material: 3 points, Dimensions: 2 points, Type: 1 point
    total_score = completeness + material_realism + dimension_validity
    format_score = (total_score / 9) * 10  # Scale to 0-10
    
    return round(format_score, 1), explanations

def check_material_type_compatibility(spec_type: str, materials: List[str]) -> bool:
    """Check if materials are compatible with the specified type."""
    material_str = ' '.join(materials).lower()
    
    # Define reasonable material combinations for types
    type_materials = {
        'table': ['wood', 'metal', 'glass', 'plastic'],
        'chair': ['wood', 'metal', 'fabric', 'leather', 'plastic'],
        'building': ['concrete', 'steel', 'glass', 'wood', 'metal'],
        'cabinet': ['wood', 'metal', 'plastic'],
        'drone': ['carbon fiber', 'plastic', 'metal', 'aluminum'],
        'sofa': ['fabric', 'leather', 'wood', 'metal'],
        'bed': ['wood', 'metal', 'fabric']
    }
    
    if spec_type not in type_materials:
        return True  # Unknown type, assume compatible
    
    suitable_materials = type_materials[spec_type]
    return any(suitable in material_str for suitable in suitable_materials)

def score_spec(spec: Dict[str, Any], prompt: str = "") -> Dict[str, Any]:
    """Main scoring function that evaluates all aspects of a spec."""
    
    # Get individual scores
    completeness_score, comp_explanations = score_completeness(spec)
    material_realism_score, mat_explanations = score_material_realism(spec)
    dimension_validity_score, dim_explanations = score_dimension_validity(spec)
    type_match_score, type_explanations = score_type_match(spec, prompt)
    
    # Calculate format score
    format_score, format_explanations = calculate_format_score(spec)
    
    # Combine all explanations
    all_explanations = []
    all_explanations.extend(comp_explanations)
    all_explanations.extend(mat_explanations)
    all_explanations.extend(dim_explanations)
    all_explanations.extend(type_explanations)
    
    return {
        "completeness_score": completeness_score,
        "material_realism_score": material_realism_score,
        "dimension_validity_score": dimension_validity_score,
        "type_match_score": type_match_score,
        "format_score": format_score,
        "explanations": all_explanations
    }

if __name__ == "__main__":
    # Test scoring with sample spec
    test_spec = {
        "type": "table",
        "material": ["wood", "metal"],
        "color": "brown",
        "dimensions": {"raw": "6x4 feet"},
        "purpose": "dining"
    }
    
    result = score_spec(test_spec, "Design a wooden dining table")
    
    print("Test scoring result:")
    print(f"Format score: {result['format_score']}")
    print(f"Completeness: {result['completeness_score']}/4")
    print(f"Material realism: {result['material_realism_score']}/3")
    print(f"Dimension validity: {result['dimension_validity_score']}/2")
    print(f"Type match: {result['type_match_score']}/1")
    print(f"Explanations: {result['explanations']}")