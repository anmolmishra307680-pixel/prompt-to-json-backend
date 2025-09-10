import pytest
from src.extractor import extract_basic_fields
from src.schema import save_spec, DesignSpec
from pydantic import ValidationError

def test_edge_case_empty_prompt():
    """Test handling of empty prompt"""
    result = extract_basic_fields("")
    assert result["type"] is None
    assert result["material"] == []
    assert result["color"] is None

def test_edge_case_whitespace_only():
    """Test handling of whitespace-only prompt"""
    result = extract_basic_fields("   \n\t  ")
    assert result["type"] is None
    assert result["material"] == []

def test_edge_case_special_characters():
    """Test handling of prompts with special characters"""
    result = extract_basic_fields("Design a @#$% building with !@# materials")
    assert result["type"] == "building"

def test_edge_case_very_long_prompt():
    """Test handling of very long prompts"""
    long_prompt = "Create a " + "very " * 100 + "long building using steel"
    result = extract_basic_fields(long_prompt)
    assert result["type"] == "building"
    assert "steel" in result["material"]

def test_edge_case_multiple_materials():
    """Test extraction of multiple materials"""
    result = extract_basic_fields("Build with steel, glass, concrete, wood, aluminum")
    expected_materials = ["steel", "glass", "concrete", "wood", "aluminum"]
    for material in expected_materials:
        assert material in result["material"]

def test_edge_case_case_sensitivity():
    """Test case insensitive matching"""
    result = extract_basic_fields("Create a BUILDING using STEEL and GLASS")
    assert result["type"] == "building"
    assert "steel" in result["material"]
    assert "glass" in result["material"]

def test_schema_edge_case_long_type_name():
    """Test schema with very long type name"""
    spec = DesignSpec(type="a" * 100)
    assert len(spec.type) == 100

def test_schema_edge_case_many_materials():
    """Test schema with many materials"""
    materials = [f"material_{i}" for i in range(50)]
    spec = DesignSpec(type="test", material=materials)
    assert len(spec.material) == 50