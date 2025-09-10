"""Unit tests for Pydantic schema validation module."""

import pytest
import sys
import tempfile
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from schema import DesignSpec, save_valid_spec, validate_and_save

class TestDesignSpec:
    """Test cases for Pydantic DesignSpec model."""
    
    def test_valid_spec_creation(self):
        """Test creating valid DesignSpec instance."""
        spec_data = {
            "type": "table",
            "material": ["wood", "metal"],
            "color": "brown",
            "dimensions": {"raw": "6x4 feet"},
            "purpose": "dining"
        }
        
        spec = DesignSpec(**spec_data)
        
        assert spec.type == "table"
        assert spec.material == ["wood", "metal"]
        assert spec.color == "brown"
        assert spec.dimensions == {"raw": "6x4 feet"}
        assert spec.purpose == "dining"
    
    def test_required_field_validation(self):
        """Test that required fields are enforced."""
        # Missing required 'type' field
        invalid_spec = {
            "material": ["wood"],
            "color": "brown"
        }
        
        with pytest.raises(Exception):  # Pydantic ValidationError
            DesignSpec(**invalid_spec)
    
    def test_optional_fields(self):
        """Test that optional fields work correctly."""
        minimal_spec = {
            "type": "chair",
            "material": ["fabric"]
        }
        
        spec = DesignSpec(**minimal_spec)
        
        assert spec.type == "chair"
        assert spec.material == ["fabric"]
        assert spec.color is None
        assert spec.dimensions is None
        assert spec.purpose is None
        assert spec.metadata is None
    
    def test_material_list_validation(self):
        """Test material list validation."""
        spec_data = {
            "type": "building",
            "material": ["concrete", "glass", "steel"]
        }
        
        spec = DesignSpec(**spec_data)
        
        assert len(spec.material) == 3
        assert "concrete" in spec.material
        assert "glass" in spec.material
        assert "steel" in spec.material
    
    def test_dimensions_dict_validation(self):
        """Test dimensions dictionary validation."""
        spec_data = {
            "type": "building",
            "material": ["concrete"],
            "dimensions": {
                "floors": 3,
                "area_m2": 500.5,
                "raw": "3-floor building"
            }
        }
        
        spec = DesignSpec(**spec_data)
        
        assert spec.dimensions["floors"] == 3
        assert spec.dimensions["area_m2"] == 500.5
        assert spec.dimensions["raw"] == "3-floor building"

class TestSaveValidSpec:
    """Test cases for save_valid_spec function."""
    
    def test_save_valid_spec_success(self):
        """Test successful spec validation and saving."""
        valid_spec = {
            "type": "table",
            "material": ["wood"],
            "color": "brown",
            "dimensions": {"raw": "6 feet"},
            "purpose": "dining"
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = save_valid_spec(valid_spec, out_dir=temp_dir, prompt="test table")
            
            assert filepath is not None
            assert os.path.exists(filepath)
            
            # Verify file contents
            import json
            with open(filepath, 'r') as f:
                saved_data = json.load(f)
            
            assert saved_data["type"] == "table"
            assert saved_data["material"] == ["wood"]
            assert "metadata" in saved_data
            assert saved_data["metadata"]["validation"] == "passed"
    
    def test_save_valid_spec_validation_error(self):
        """Test handling of validation errors."""
        invalid_spec = {
            "material": ["wood"],  # Missing required 'type'
            "color": "brown"
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = save_valid_spec(invalid_spec, out_dir=temp_dir)
            
            assert filepath is None
            
            # Check that error was logged
            assert os.path.exists("reports/validation_errors.txt")
    
    def test_save_valid_spec_filename_generation(self):
        """Test filename generation with slug and timestamp."""
        valid_spec = {
            "type": "chair",
            "material": ["metal"]
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = save_valid_spec(valid_spec, out_dir=temp_dir, prompt="Design a metal chair")
            
            assert filepath is not None
            filename = os.path.basename(filepath)
            
            # Should contain slug and timestamp
            assert "design_a_metal_chair" in filename
            assert filename.endswith(".json")
    
    def test_save_valid_spec_metadata_addition(self):
        """Test automatic metadata addition."""
        valid_spec = {
            "type": "cabinet",
            "material": ["wood"]
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            filepath = save_valid_spec(valid_spec, out_dir=temp_dir)
            
            import json
            with open(filepath, 'r') as f:
                saved_data = json.load(f)
            
            metadata = saved_data["metadata"]
            assert metadata["validation"] == "passed"
            assert metadata["schema_version"] == "1.0"
            assert "timestamp" in metadata

class TestValidateAndSave:
    """Test cases for legacy validate_and_save function."""
    
    def test_validate_and_save_success(self):
        """Test successful validation and saving with legacy function."""
        valid_data = {
            "type": "shelf",
            "material": ["wood"],
            "color": "white",
            "dimensions": {"raw": "standard"},
            "purpose": "storage"
        }
        
        with tempfile.TemporaryDirectory():
            # Change to temp directory for test
            original_cwd = os.getcwd()
            try:
                os.makedirs("spec_outputs", exist_ok=True)
                spec = validate_and_save(valid_data, "test_shelf.json")
                
                assert spec is not None
                assert spec.type == "shelf"
                assert spec.material == ["wood"]
                assert os.path.exists("spec_outputs/test_shelf.json")
                
            finally:
                os.chdir(original_cwd)
    
    def test_validate_and_save_validation_error(self):
        """Test validation error handling in legacy function."""
        invalid_data = {
            "material": ["plastic"],  # Missing required 'type'
            "color": "blue"
        }
        
        spec = validate_and_save(invalid_data, "invalid_spec.json")
        
        assert spec is None

class TestSchemaEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_material_list(self):
        """Test handling of empty material list."""
        spec_data = {
            "type": "table",
            "material": []  # Empty list
        }
        
        spec = DesignSpec(**spec_data)
        assert spec.material == []
    
    def test_none_values_handling(self):
        """Test handling of None values in optional fields."""
        spec_data = {
            "type": "chair",
            "material": ["fabric"],
            "color": None,
            "dimensions": None,
            "purpose": None
        }
        
        spec = DesignSpec(**spec_data)
        assert spec.color is None
        assert spec.dimensions is None
        assert spec.purpose is None
    
    def test_complex_dimensions_structure(self):
        """Test complex dimensions dictionary structure."""
        spec_data = {
            "type": "building",
            "material": ["concrete"],
            "dimensions": {
                "floors": 5,
                "area_m2": 1000.0,
                "raw": "5-floor office building",
                "length_m": 50,
                "width_m": 20,
                "custom_field": "additional info"
            }
        }
        
        spec = DesignSpec(**spec_data)
        dims = spec.dimensions
        
        assert dims["floors"] == 5
        assert dims["area_m2"] == 1000.0
        assert dims["custom_field"] == "additional info"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])