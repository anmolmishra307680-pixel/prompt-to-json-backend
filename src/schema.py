from pydantic import BaseModel, ValidationError
from typing import List, Optional, Dict, Any
import json
import os
import re
from datetime import datetime

class DesignSpec(BaseModel):
    """Pydantic model for design specifications with strict validation."""
    type: str
    material: List[str]
    color: Optional[str] = None
    dimensions: Optional[Dict[str, Any]] = None  # floors, area_m2, raw
    purpose: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

def create_slug(text: str) -> str:
    """Create URL-friendly slug from text."""
    slug = re.sub(r'[^\w\s-]', '', text.lower())
    slug = re.sub(r'[-\s]+', '_', slug)
    return slug[:30]

def save_valid_spec(spec: dict, out_dir: str = "spec_outputs", prompt: str = "") -> Optional[str]:
    """Validate spec with Pydantic and save to file."""
    try:
        # Validate with Pydantic
        validated_spec = DesignSpec(**spec)
        
        # Create filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        if prompt:
            slug = create_slug(prompt)
            filename = f"{slug}_{timestamp}.json"
        else:
            filename = f"spec_{timestamp}.json"
        
        # Save validated spec
        os.makedirs(out_dir, exist_ok=True)
        filepath = os.path.join(out_dir, filename)
        
        # Add metadata
        output_data = validated_spec.dict()
        output_data["metadata"] = {
            "timestamp": datetime.now().isoformat(),
            "validation": "passed",
            "schema_version": "1.0"
        }
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"[VALID] Spec saved to: {filepath}")
        return filepath
        
    except ValidationError as e:
        # Log validation errors
        error_msg = f"Validation failed for spec: {spec}\nErrors: {e}\nTimestamp: {datetime.now().isoformat()}\n\n"
        
        os.makedirs("reports", exist_ok=True)
        with open("reports/validation_errors.txt", "a", encoding='utf-8') as f:
            f.write(error_msg)
        
        print(f"[ERROR] Validation failed: {e}")
        return None
    
    except Exception as e:
        print(f"[ERROR] Failed to save spec: {e}")
        return None

def validate_and_save(data: dict, filename: str) -> Optional[DesignSpec]:
    """Legacy function for backward compatibility."""
    try:
        spec = DesignSpec(**data)
        
        os.makedirs("spec_outputs", exist_ok=True)
        filepath = f"spec_outputs/{filename}"
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(spec.dict(), f, indent=2, ensure_ascii=False)
        
        return spec
    except ValidationError as e:
        print(f"Validation error: {e}")
        return None

if __name__ == "__main__":
    # Test validation with new schema
    test_specs = [
        {
            "type": "table",
            "material": ["wood"],
            "color": "brown",
            "dimensions": {"raw": "6 feet"},
            "purpose": "dining"
        },
        {
            "type": "building",
            "material": ["glass", "concrete"],
            "color": "none",
            "dimensions": {"floors": 2, "raw": "2-floor"},
            "purpose": "library"
        },
        {
            # Invalid spec - missing required fields
            "material": ["metal"],
            "color": "red"
        }
    ]
    
    print("=== Pydantic Schema Validation Test ===")
    
    for i, spec in enumerate(test_specs, 1):
        print(f"\nTest {i}: {spec}")
        result = save_valid_spec(spec, prompt=f"test_spec_{i}")
        if result:
            print(f"Success: {result}")
        else:
            print("Failed validation")