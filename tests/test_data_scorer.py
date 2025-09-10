"""Unit tests for data_scorer.py quality scoring module."""

import pytest
import sys
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from data_scorer import score_spec

# Import individual functions for testing
try:
    from data_scorer import (
        score_completeness,
        score_material_realism,
        score_dimension_validity,
        score_type_match,
        calculate_format_score
    )
except ImportError:
    # Functions not exported, skip individual tests
    score_completeness = None
    score_material_realism = None
    score_dimension_validity = None
    score_type_match = None
    calculate_format_score = None

class TestDataScorer:
    """Test cases for data scoring functionality."""
    
    def test_perfect_spec_scoring(self):
        """Test scoring of a perfect specification."""
        perfect_spec = {
            "type": "table",
            "material": ["wood"],
            "color": "brown",
            "dimensions": {"raw": "6x4 feet", "area_m2": 2.2},
            "purpose": "dining"
        }
        
        result = score_spec(perfect_spec, "Design a wooden dining table")
        
        assert result['completeness_score'] == 4  # All fields present
        assert result['material_realism_score'] >= 2  # Good material
        assert result['dimension_validity_score'] >= 1  # Has units
        assert result['type_match_score'] == 1  # Type matches prompt
        assert result['format_score'] >= 8.0  # High overall score
    
    def test_incomplete_spec_scoring(self):
        """Test scoring of an incomplete specification."""
        incomplete_spec = {
            "type": "chair",
            "material": ["unknown_material"],
            "color": "blue"
            # Missing dimensions and purpose
        }
        
        result = score_spec(incomplete_spec, "Create a chair")
        
        assert result['completeness_score'] <= 2  # Missing fields
        assert result['material_realism_score'] <= 1  # Unknown material
        assert result['dimension_validity_score'] == 0  # No dimensions
        assert result['type_match_score'] == 1  # Type matches
        assert result['format_score'] <= 5.0  # Low overall score
    
    def test_building_spec_scoring(self):
        """Test scoring of a building specification."""
        building_spec = {
            "type": "building",
            "material": ["concrete", "glass"],
            "dimensions": {"floors": 3, "raw": "3-floor"},
            "purpose": "library"
        }
        
        result = score_spec(building_spec, "Build a 3-floor library")
        
        assert result['completeness_score'] >= 3  # Most fields present
        assert result['material_realism_score'] >= 2  # Good materials for building
        assert result['dimension_validity_score'] >= 1  # Has floor count
        assert result['type_match_score'] == 1  # Type matches
        assert result['format_score'] >= 7.0  # Good overall score
    
    def test_unreasonable_dimensions(self):
        """Test scoring with unreasonable dimensions."""
        unreasonable_spec = {
            "type": "building",
            "material": ["concrete"],
            "dimensions": {"floors": 100, "area_m2": 50000},  # Unreasonable values
            "purpose": "office"
        }
        
        result = score_spec(unreasonable_spec, "Build an office building")
        
        assert result['dimension_validity_score'] <= 1  # Unreasonable dimensions
        assert "unreasonable" in ' '.join(result['explanations']).lower()
    
    def test_multi_material_scoring(self):
        """Test scoring with multiple materials."""
        multi_material_spec = {
            "type": "table",
            "material": ["wood", "metal", "glass"],
            "dimensions": {"raw": "8 feet long"},
            "purpose": "dining"
        }
        
        result = score_spec(multi_material_spec, "Design a dining table")
        
        assert result['completeness_score'] == 4  # All fields present
        assert result['material_realism_score'] >= 2  # Multiple materials OK
        assert "multi-material" in ' '.join(result['explanations']).lower()

class TestIndividualScorers:
    """Test individual scoring functions."""
    
    @pytest.mark.skipif(score_completeness is None, reason="Individual functions not exported")
    def test_completeness_scoring(self):
        """Test completeness scoring function."""
        complete_spec = {
            "type": "chair",
            "material": ["wood"],
            "dimensions": {"raw": "standard"},
            "purpose": "dining"
        }
        
        score, explanations = score_completeness(complete_spec)
        assert score == 4
        assert "type specified" in explanations
        assert "material specified" in explanations
        assert "dimensions provided" in explanations
        assert "purpose specified" in explanations
    
    @pytest.mark.skipif(score_material_realism is None, reason="Individual functions not exported")
    def test_material_realism_scoring(self):
        """Test material realism scoring function."""
        good_material_spec = {
            "type": "table",
            "material": ["wood", "metal"]
        }
        
        score, explanations = score_material_realism(good_material_spec)
        assert score >= 2
        assert "materials recognized" in ' '.join(explanations)
    
    @pytest.mark.skipif(score_dimension_validity is None, reason="Individual functions not exported")
    def test_dimension_validity_scoring(self):
        """Test dimension validity scoring function."""
        good_dimensions_spec = {
            "dimensions": {"raw": "6x4 feet", "area_m2": 2.2}
        }
        
        score, explanations = score_dimension_validity(good_dimensions_spec)
        assert score >= 1
        assert "units" in ' '.join(explanations).lower()
    
    @pytest.mark.skipif(score_type_match is None, reason="Individual functions not exported")
    def test_type_match_scoring(self):
        """Test type match scoring function."""
        matching_spec = {"type": "table"}
        
        score, explanations = score_type_match(matching_spec, "Design a dining table")
        assert score == 1
        assert "matches prompt" in ' '.join(explanations)
        
        non_matching_spec = {"type": "drone"}
        score, explanations = score_type_match(non_matching_spec, "Design a dining table")
        assert score == 0
        assert "may not match" in ' '.join(explanations)

class TestEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_empty_spec_scoring(self):
        """Test scoring of empty specification."""
        empty_spec = {}
        
        result = score_spec(empty_spec, "Design something")
        
        assert result['completeness_score'] == 0
        assert result['material_realism_score'] == 0
        assert result['dimension_validity_score'] == 0
        assert result['type_match_score'] == 0
        assert result['format_score'] == 0.0
    
    def test_none_values_spec(self):
        """Test scoring with None values."""
        none_spec = {
            "type": None,
            "material": None,
            "dimensions": None,
            "purpose": None
        }
        
        result = score_spec(none_spec, "Design something")
        
        assert result['completeness_score'] == 0
        assert result['format_score'] <= 2.0
    
    def test_string_material_format(self):
        """Test scoring with string material format."""
        string_material_spec = {
            "type": "chair",
            "material": "wood",  # String instead of list
            "dimensions": {"raw": "standard size"},
            "purpose": "dining"
        }
        
        result = score_spec(string_material_spec, "Design a wooden chair")
        
        assert result['completeness_score'] >= 3
        assert result['material_realism_score'] >= 1

if __name__ == "__main__":
    pytest.main([__file__, "-v"])