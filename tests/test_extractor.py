"""Unit tests for extractor.py with improved regex parsing."""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from extractor import extract_basic_fields, parse_dimensions

class TestExtractor:
    """Test cases for the improved extractor."""
    
    def test_library_with_floors_and_materials(self):
        """Test extraction of 2-floor library with multiple materials."""
        prompt = "Design a 2-floor library using glass and concrete"
        result = extract_basic_fields(prompt)
        
        assert result['type'] == 'building'
        assert 'glass' in result['material']
        assert 'concrete' in result['material']
        assert result['dimensions']['floors'] == 2
        assert result['dimensions']['raw'] == '2-floor'
        assert result['purpose'] == 'library'
    
    def test_wooden_table_with_dimensions(self):
        """Test extraction of wooden table with specific dimensions."""
        prompt = "Create a wooden dining table 6 feet long and brown"
        result = extract_basic_fields(prompt)
        
        assert result['type'] == 'table'
        assert 'wood' in result['material']
        assert result['color'] == 'brown'
        assert result['dimensions']['raw'] == '6 feet'
        assert result['purpose'] == 'dining'
    
    def test_medical_cabinet_steel(self):
        """Test extraction of steel medical cabinet."""
        prompt = "Build a steel cabinet for medical storage"
        result = extract_basic_fields(prompt)
        
        assert result['type'] == 'cabinet'
        assert 'metal' in result['material']  # steel maps to metal
        assert result['purpose'] in ['medical', 'storage']  # Both are valid
        assert isinstance(result['material'], list)
    
    def test_office_with_area(self):
        """Test extraction of office with area in square meters.""" 
        prompt = "Make a 50 sqm office with aluminum frame"
        result = extract_basic_fields(prompt)
        
        assert 'metal' in result['material']  # aluminum maps to metal
        assert result['dimensions']['area_m2'] == 50.0
        assert result['dimensions']['raw'] == '50 sqm'
        assert result['purpose'] == 'office'
    
    def test_multi_floor_building(self):
        """Test extraction of 3-floor building with glass."""
        prompt = "Design a 3-floor building with glass walls"
        result = extract_basic_fields(prompt)
        
        assert result['type'] == 'building'
        assert 'glass' in result['material']
        assert result['dimensions']['floors'] == 3
        assert result['dimensions']['raw'] == '3-floor'

class TestDimensionParsing:
    """Test cases for dimension parsing function."""
    
    def test_floor_parsing(self):
        """Test floor count extraction."""
        result = parse_dimensions("2-floor building")
        assert result['floors'] == 2
        assert result['raw'] == '2-floor'
    
    def test_area_parsing_sqm(self):
        """Test area parsing in square meters."""
        result = parse_dimensions("50 sqm office")
        assert result['area_m2'] == 50.0
        assert result['raw'] == '50 sqm'
    
    def test_area_parsing_sqft(self):
        """Test area parsing in square feet with conversion."""
        result = parse_dimensions("100 sqft room")
        assert abs(result['area_m2'] - 9.29) < 0.01  # 100 sqft ≈ 9.29 sqm
    
    def test_no_dimensions(self):
        """Test parsing text with no dimensions."""
        result = parse_dimensions("wooden table")
        assert result['floors'] is None
        assert result['area_m2'] is None
        assert result['raw'] is None

if __name__ == "__main__":
    pytest.main([__file__, "-v"])