from pydantic import BaseModel
from typing import Optional
import json
import os

class DesignSpec(BaseModel):
    """Pydantic model for furniture design specifications."""
    type: Optional[str] = None        # Furniture type (table, chair, etc.)
    material: Optional[str] = None    # Material (wood, metal, etc.)
    color: Optional[str] = None       # Color specification
    dimensions: Optional[str] = None  # Size measurements
    purpose: Optional[str] = None     # Intended use/room

def validate_and_save(raw_dict, filename):
    """Validate raw dictionary against schema and save to spec_outputs folder."""
    # Create validated DesignSpec instance
    spec = DesignSpec(**raw_dict)
    
    # Ensure output directory exists
    os.makedirs("spec_outputs", exist_ok=True)
    
    # Save validated spec as JSON
    with open(f"spec_outputs/{filename}", 'w') as f:
        json.dump(spec.dict(), f, indent=2)
    
    return spec

if __name__ == "__main__":
    # Example raw dict to validate
    example_dict = {
        "type": "table",
        "material": "wood",
        "color": "brown",
        "dimensions": "6 feet",
        "purpose": "dining"
    }
    
    print("Validating example dict:", example_dict)
    validated_spec = validate_and_save(example_dict, "dining_table_spec.json")
    print("Validation successful:", validated_spec)
    print("Saved to spec_outputs/dining_table_spec.json")