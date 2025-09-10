import pytest
import os
import json
from src.extractor import extract_basic_fields
from src.schema import save_spec, DesignSpec

def test_extractor_to_schema_integration():
    """Test full pipeline from extractor to schema save"""
    prompt = "Design a 2-floor building using glass and concrete."
    
    # Extract fields
    extracted = extract_basic_fields(prompt)
    
    # Validate extraction worked
    assert extracted["type"] == "building"
    assert "glass" in extracted["material"]
    assert "concrete" in extracted["material"]
    assert extracted["dimensions"] == "2-floor"
    
    # Save to schema
    filename = save_spec(extracted, "data/spec_outputs/test_integration.json")
    
    # Verify file was created and is valid
    assert os.path.exists(filename)
    with open(filename, 'r') as f:
        saved_data = json.load(f)
    
    # Verify schema structure
    spec = DesignSpec(**saved_data)
    assert spec.type == "building"
    assert "glass" in spec.material
    assert "concrete" in spec.material

def test_integration_with_minimal_extraction():
    """Test integration when extractor finds minimal fields"""
    prompt = "Something unknown and unrecognized."
    
    extracted = extract_basic_fields(prompt)
    
    # Should have mostly None/empty values
    assert extracted["type"] is None
    assert extracted["material"] == []
    
    # This should fail validation due to missing type
    with pytest.raises(Exception):  # ValidationError or similar
        save_spec(extracted)

def test_integration_with_fallback():
    """Test integration with fallback values for missing fields"""
    prompt = "Something unknown and unrecognized."
    
    extracted = extract_basic_fields(prompt)
    
    # Add fallback logic
    if extracted["type"] is None:
        extracted["type"] = "unspecified"
    if not extracted["material"]:
        extracted["material"] = ["unspecified"]
    
    # Should now work with fallbacks
    filename = save_spec(extracted, "data/spec_outputs/test_fallback.json")
    assert os.path.exists(filename)
    
    with open(filename, 'r') as f:
        saved_data = json.load(f)
    
    assert saved_data["type"] == "unspecified"
    assert saved_data["material"] == ["unspecified"]