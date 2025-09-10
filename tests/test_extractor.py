import pytest
from src.extractor import extract_basic_fields

def test_building_with_materials():
    prompt = "Design a 2-floor building using glass and concrete."
    result = extract_basic_fields(prompt)
    
    assert result["type"] == "building"
    assert "glass" in result["material"]
    assert "concrete" in result["material"]
    assert result["dimensions"] == "2-floor"

def test_gearbox_with_color_and_material():
    prompt = "Create a red gearbox with steel gears."
    result = extract_basic_fields(prompt)
    
    assert result["type"] == "gearbox"
    assert result["color"] == "red"
    assert "steel" in result["material"]

def test_throne_with_purpose():
    prompt = "Model a medieval throne for a fantasy game."
    result = extract_basic_fields(prompt)
    
    assert result["type"] == "throne"
    assert result["purpose"] == "a fantasy game"

def test_no_matches():
    prompt = "Something completely different."
    result = extract_basic_fields(prompt)
    
    assert result["type"] is None
    assert result["material"] == []
    assert result["color"] is None
    assert result["dimensions"] is None
    assert result["purpose"] is None

def test_multiple_colors_first_match():
    prompt = "Create a blue and red house."
    result = extract_basic_fields(prompt)
    
    assert result["type"] == "house"
    assert result["color"] == "blue"

def test_dimensions_with_units():
    prompt = "Build a 15x20cm wooden chest."
    result = extract_basic_fields(prompt)
    
    assert result["type"] == "chest"
    assert "wood" in result["material"]
    assert result["dimensions"] == "15x20cm"