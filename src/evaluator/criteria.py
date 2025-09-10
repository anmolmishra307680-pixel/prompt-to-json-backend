"""Evaluation criteria and validation rules for design specifications."""

import re
from typing import List, Dict, Any, Tuple

# Known materials with categories
KNOWN_MATERIALS = {
    "wood": ["wood", "wooden", "oak", "pine", "mahogany", "cedar", "birch", "maple"],
    "metal": ["metal", "steel", "aluminum", "iron", "copper", "brass", "stainless steel", "titanium"],
    "glass": ["glass", "crystal", "tempered glass", "laminated glass"],
    "plastic": ["plastic", "polymer", "acrylic", "polycarbonate", "PVC"],
    "fabric": ["fabric", "cloth", "textile", "cotton", "linen", "silk", "wool"],
    "leather": ["leather", "hide", "suede", "faux leather"],
    "concrete": ["concrete", "cement", "reinforced concrete"],
    "composite": ["carbon fiber", "carbon fibre", "fiberglass", "composite"],
    "stone": ["marble", "granite", "limestone", "sandstone", "slate"],
    "ceramic": ["ceramic", "porcelain", "tile", "clay"]
}

# Flatten for easy lookup
ALL_MATERIALS = [material for materials in KNOWN_MATERIALS.values() for material in materials]

# Reasonable dimension ranges
DIMENSION_LIMITS = {
    "floors": {"min": 1, "max": 50},
    "area_m2": {"min": 0.1, "max": 10000},
    "area_sqft": {"min": 1, "max": 100000},
    "length_m": {"min": 0.1, "max": 100},
    "length_ft": {"min": 0.3, "max": 300}
}

# Type-specific validation rules
TYPE_RULES = {
    "table": {
        "required_fields": ["material", "dimensions"],
        "typical_materials": ["wood", "metal", "glass"],
        "typical_purposes": ["dining", "office", "coffee", "side"]
    },
    "chair": {
        "required_fields": ["material"],
        "typical_materials": ["wood", "metal", "fabric", "leather", "plastic"],
        "typical_purposes": ["dining", "office", "lounge", "outdoor"]
    },
    "building": {
        "required_fields": ["material", "dimensions"],
        "typical_materials": ["concrete", "steel", "glass", "wood"],
        "typical_purposes": ["residential", "commercial", "library", "office"]
    },
    "cabinet": {
        "required_fields": ["material", "purpose"],
        "typical_materials": ["wood", "metal", "plastic"],
        "typical_purposes": ["storage", "kitchen", "bathroom", "office"]
    }
}

def check_type_presence(spec: Dict[str, Any]) -> Tuple[bool, str]:
    """Check if type is present and valid."""
    spec_type = spec.get('type')
    
    if not spec_type or spec_type in ['unknown', 'unspecified']:
        return False, "Type specification is missing or unclear"
    
    return True, ""

def check_material_validity(spec: Dict[str, Any]) -> Tuple[bool, str]:
    """Check if materials are valid and realistic."""
    material = spec.get('material', [])
    
    if isinstance(material, str):
        material = [material]
    
    if not material or not any(m.strip() for m in material):
        return False, "Material not specified"
    
    # Check if materials are recognized
    unrecognized = []
    for mat in material:
        mat_lower = mat.lower().strip()
        if mat_lower not in ['none', 'default', 'unspecified']:
            # Check exact match or partial match
            if not any(known.lower() == mat_lower or mat_lower in known.lower() for known in ALL_MATERIALS):
                unrecognized.append(mat)
    
    if unrecognized:
        return False, f"Unrecognized materials: {', '.join(unrecognized)}"
    
    return True, ""

def check_dimensions_validity(spec: Dict[str, Any]) -> Tuple[bool, str]:
    """Check if dimensions are present and reasonable."""
    dimensions = spec.get('dimensions')
    
    if not dimensions:
        return False, "Dimensions are missing"
    
    if isinstance(dimensions, str):
        if dimensions in ['standard', 'default', 'None', '']:
            return False, "Dimensions are missing (provide specific measurements)"
        
        # Check for units
        if not any(unit in dimensions.lower() for unit in ['feet', 'ft', 'cm', 'm', 'inches', 'in', 'floor']):
            return False, "Dimensions format unclear or missing units"
        
        return True, ""
    
    if isinstance(dimensions, dict):
        raw = dimensions.get('raw', '')
        floors = dimensions.get('floors')
        area_m2 = dimensions.get('area_m2')
        
        # Check floors reasonableness
        if floors is not None:
            if floors < DIMENSION_LIMITS["floors"]["min"] or floors > DIMENSION_LIMITS["floors"]["max"]:
                return False, f"Floor count ({floors}) is unreasonable (should be 1-50)"
        
        # Check area reasonableness
        if area_m2 is not None:
            if area_m2 < DIMENSION_LIMITS["area_m2"]["min"] or area_m2 > DIMENSION_LIMITS["area_m2"]["max"]:
                return False, f"Area ({area_m2} m²) is unreasonable"
        
        # Check if raw dimensions have units
        if raw and raw not in ['None', '']:
            if not any(unit in raw.lower() for unit in ['feet', 'ft', 'cm', 'm', 'inches', 'in', 'floor']):
                return False, "Dimensions format unclear or missing units"
        elif not floors and not area_m2:
            return False, "Dimensions are missing (provide specific measurements)"
    
    return True, ""

def check_purpose_consistency(spec: Dict[str, Any], prompt: str) -> Tuple[bool, str]:
    """Check if purpose is specified and consistent."""
    purpose = str(spec.get('purpose', '')).lower().strip()
    
    if not purpose or purpose in ['general', 'unspecified']:
        return False, "Purpose or intended use not specified"
    
    # Check type-purpose consistency
    spec_type = str(spec.get('type', '')).lower()
    if spec_type in TYPE_RULES:
        typical_purposes = TYPE_RULES[spec_type].get('typical_purposes', [])
        if typical_purposes and not any(tp in purpose for tp in typical_purposes):
            # This is a warning, not an error
            pass
    
    return True, ""

def check_eco_requirements(spec: Dict[str, Any], prompt: str) -> Tuple[bool, str]:
    """Check eco-friendly requirements if mentioned in prompt."""
    if not any(eco_word in prompt.lower() for eco_word in ['eco', 'green', 'sustainable', 'environment']):
        return True, ""  # No eco requirements
    
    spec_str = str(spec).lower()
    if not any(eco_feature in spec_str for eco_feature in ['energy', 'sustainable', 'eco', 'green', 'solar', 'recycled']):
        return False, "No mention of energy efficiency or sustainable features"
    
    return True, ""

def check_type_specific_requirements(spec: Dict[str, Any]) -> Tuple[bool, str]:
    """Check type-specific requirements."""
    spec_type = str(spec.get('type', '')).lower()
    
    if spec_type not in TYPE_RULES:
        return True, ""  # No specific rules for this type
    
    rules = TYPE_RULES[spec_type]
    missing_fields = []
    
    for field in rules.get('required_fields', []):
        if not spec.get(field) or spec.get(field) in ['unspecified', 'default', 'none']:
            missing_fields.append(field)
    
    if missing_fields:
        return False, f"Missing required fields for {spec_type}: {', '.join(missing_fields)}"
    
    return True, ""

def generate_recommendations(issues: List[str], spec: Dict[str, Any], prompt: str) -> List[str]:
    """Generate specific recommendations based on issues."""
    recommendations = []
    
    if "type_missing" in issues:
        recommendations.append("Specify the type of object (e.g., table, chair, building)")
    
    if "material_missing" in issues:
        recommendations.append("Add material specifications (e.g., wood, metal, glass)")
    
    if "material_unrecognized" in issues:
        recommendations.append("Use standard material names from known categories")
    
    if "dimensions_missing" in issues:
        recommendations.append("Provide specific measurements with units (e.g., '6 feet', '2 meters')")
    
    if "dimensions_unparseable" in issues:
        recommendations.append("Include units in dimensions (feet, meters, cm, etc.)")
    
    if "purpose_missing" in issues:
        recommendations.append("Specify the intended use or purpose")
    
    if "energy_source_missing" in issues:
        recommendations.append("Add sustainable or energy-efficient features as requested")
    
    # Type-specific recommendations
    spec_type = str(spec.get('type', '')).lower()
    if spec_type == "building" and "floors" not in str(spec.get('dimensions', {})):
        recommendations.append("Specify number of floors for building")
    
    if spec_type in ["table", "chair"] and not spec.get('dimensions'):
        recommendations.append(f"Add dimensions appropriate for {spec_type} (length, width, height)")
    
    return recommendations