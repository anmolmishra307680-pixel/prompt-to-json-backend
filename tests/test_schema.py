import pytest
import os
import json
from pydantic import ValidationError
from src.schema import DesignSpec, save_spec

def test_design_spec_valid():
    """Test valid DesignSpec creation"""
    spec = DesignSpec(
        type="gearbox",
        material=["steel", "aluminum"],
        color="red",
        dimensions="15x15cm",
        purpose="automotive"
    )
    assert spec.type == "gearbox"
    assert spec.material == ["steel", "aluminum"]
    assert spec.color == "red"

def test_design_spec_minimal():
    """Test DesignSpec with only required fields"""
    spec = DesignSpec(type="building")
    assert spec.type == "building"
    assert spec.material == []
    assert spec.color is None

def test_design_spec_invalid_empty_type():
    """Test that empty type raises ValidationError"""
    with pytest.raises(ValidationError):
        DesignSpec(type="")
    
    with pytest.raises(ValidationError):
        DesignSpec(type="   ")

def test_design_spec_missing_type():
    """Test that missing type raises ValidationError"""
    with pytest.raises(ValidationError):
        DesignSpec(material=["steel"])

def test_save_spec_with_filename():
    """Test save_spec with custom filename"""
    raw = {
        "type": "gearbox",
        "material": ["steel"],
        "dimensions": "15x15cm",
        "purpose": "automotive"
    }
    filename = save_spec(raw, "data/spec_outputs/test_gearbox.json")
    
    assert os.path.exists(filename)
    with open(filename, 'r') as f:
        saved_data = json.load(f)
    
    assert saved_data["type"] == "gearbox"
    assert saved_data["material"] == ["steel"]

def test_save_spec_auto_filename():
    """Test save_spec with automatic filename generation"""
    raw = {
        "type": "medieval throne",
        "material": ["wood"],
        "color": "brown"
    }
    filename = save_spec(raw)
    
    assert "medieval_throne.json" in filename
    assert os.path.exists(filename)

def test_save_spec_creates_directory():
    """Test that save_spec creates spec_outputs directory if it doesn't exist"""
    # Remove directory if it exists
    import shutil
    if os.path.exists("data/spec_outputs"):
        shutil.rmtree("data/spec_outputs")
    
    raw = {"type": "test_object"}
    filename = save_spec(raw)
    
    assert os.path.exists("data/spec_outputs")
    assert os.path.exists(filename)