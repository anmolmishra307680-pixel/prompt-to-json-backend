"""Unit tests for evaluator module."""

import pytest
import sys
import tempfile
import os
from pathlib import Path

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

from evaluator.report import evaluate_spec, save_report, calculate_completeness_score
from evaluator.criteria import check_type_presence, check_material_validity, check_dimensions_validity
from evaluator.feedback import generate_feedback

class TestEvaluateSpec:
    """Test cases for spec evaluation functionality."""
    
    def test_evaluate_perfect_spec(self):
        """Test evaluation of a perfect specification."""
        prompt = "Design a wooden dining table"
        spec = {
            "type": "table",
            "material": ["wood"],
            "color": "brown",
            "dimensions": {"raw": "6x4 feet"},
            "purpose": "dining"
        }
        
        report = evaluate_spec(prompt, spec)
        
        assert report["severity"] == "none"
        assert len(report["issues"]) == 0
        assert "complete and well-defined" in report["critic_feedback"]
        assert len(report["recommendations"]) == 0
    
    def test_evaluate_incomplete_spec(self):
        """Test evaluation of incomplete specification."""
        prompt = "Create a chair"
        spec = {
            "type": "chair",
            "material": ["unknown_material"],
            "color": "blue"
            # Missing dimensions and purpose
        }
        
        report = evaluate_spec(prompt, spec)
        
        assert report["severity"] in ["minor", "major"]
        assert len(report["issues"]) > 0
        assert len(report["recommendations"]) > 0
        assert "quality_scores" in report
    
    def test_evaluate_building_spec(self):
        """Test evaluation of building specification."""
        prompt = "Build a 3-floor library"
        spec = {
            "type": "building",
            "material": ["concrete", "glass"],
            "dimensions": {"floors": 3, "raw": "3-floor"},
            "purpose": "library"
        }
        
        report = evaluate_spec(prompt, spec)
        
        assert report["severity"] in ["none", "minor"]
        assert "quality_scores" in report
        assert report["quality_scores"]["format_score"] > 5.0
    
    def test_evaluate_eco_friendly_requirements(self):
        """Test evaluation with eco-friendly requirements."""
        prompt = "Design an eco-friendly sustainable office building"
        spec = {
            "type": "building",
            "material": ["concrete"],
            "dimensions": {"floors": 2},
            "purpose": "office"
            # Missing eco-friendly features
        }
        
        report = evaluate_spec(prompt, spec)
        
        # Should detect missing eco-friendly features
        assert any("energy" in issue or "sustainable" in issue for issue in report["issues"])

class TestSaveReport:
    """Test cases for report saving functionality."""
    
    def test_save_report_json_and_txt(self):
        """Test saving report in both JSON and TXT formats."""
        report = {
            "prompt": "Design a table",
            "timestamp": "2025-01-10T10:00:00",
            "critic_feedback": "Test feedback",
            "issues": ["test_issue"],
            "severity": "minor",
            "recommendations": ["test recommendation"],
            "quality_scores": {"format_score": 7.5},
            "spec_summary": {"type": "table"}
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path, txt_path = save_report(report, output_dir=temp_dir)
            
            # Check JSON file
            assert os.path.exists(json_path)
            import json
            with open(json_path, 'r') as f:
                saved_report = json.load(f)
            assert saved_report["prompt"] == "Design a table"
            
            # Check TXT file
            assert os.path.exists(txt_path)
            with open(txt_path, 'r') as f:
                txt_content = f.read()
            assert "DESIGN SPECIFICATION EVALUATION REPORT" in txt_content
            assert "Test feedback" in txt_content
    
    def test_save_report_filename_generation(self):
        """Test report filename generation."""
        report = {
            "prompt": "Create a modern steel chair",
            "timestamp": "2025-01-10T10:00:00",
            "critic_feedback": "Good spec",
            "issues": [],
            "severity": "none",
            "recommendations": [],
            "spec_summary": {"type": "chair"}
        }
        
        with tempfile.TemporaryDirectory() as temp_dir:
            json_path, txt_path = save_report(report, output_dir=temp_dir)
            
            json_filename = os.path.basename(json_path)
            txt_filename = os.path.basename(txt_path)
            
            # Should contain slug from prompt
            assert "create_a_modern_steel_chair" in json_filename
            assert "create_a_modern_steel_chair" in txt_filename

class TestEvaluatorCriteria:
    """Test cases for individual evaluation criteria."""
    
    def test_check_type_presence_valid(self):
        """Test type presence check with valid type."""
        spec = {"type": "table"}
        
        is_valid, message = check_type_presence(spec)
        
        assert is_valid is True
        assert message == ""
    
    def test_check_type_presence_invalid(self):
        """Test type presence check with invalid type."""
        spec = {"type": "unknown"}
        
        is_valid, message = check_type_presence(spec)
        
        assert is_valid is False
        assert "missing or unclear" in message.lower()
    
    def test_check_material_validity_valid(self):
        """Test material validity check with valid materials."""
        spec = {"material": ["wood", "metal"]}
        
        is_valid, message = check_material_validity(spec)
        
        assert is_valid is True
        assert message == ""
    
    def test_check_material_validity_invalid(self):
        """Test material validity check with invalid materials."""
        spec = {"material": ["unknown_material"]}
        
        is_valid, message = check_material_validity(spec)
        
        assert is_valid is False
        assert "unrecognized" in message.lower()
    
    def test_check_dimensions_validity_valid(self):
        """Test dimensions validity check with valid dimensions."""
        spec = {"dimensions": {"raw": "6x4 feet", "floors": 2}}
        
        is_valid, message = check_dimensions_validity(spec)
        
        assert is_valid is True
        assert message == ""
    
    def test_check_dimensions_validity_invalid(self):
        """Test dimensions validity check with invalid dimensions."""
        spec = {"dimensions": {"raw": "standard"}}
        
        is_valid, message = check_dimensions_validity(spec)
        
        assert is_valid is False
        assert "missing" in message.lower()

class TestFeedbackGeneration:
    """Test cases for feedback generation."""
    
    def test_generate_feedback_for_incomplete_spec(self):
        """Test feedback generation for incomplete spec."""
        prompt = "Design a table"
        spec = {
            "type": "table",
            "material": ["unknown"],
            "color": "brown"
        }
        report = {
            "issues": ["material_invalid", "dimensions_missing"],
            "severity": "minor",
            "quality_scores": {"completeness_score": 2}
        }
        
        feedback = generate_feedback(prompt, spec, report)
        
        assert "feedback_text" in feedback
        assert "actions" in feedback
        assert len(feedback["actions"]) > 0
        assert feedback["source"] == "heuristic"
    
    def test_generate_feedback_for_good_spec(self):
        """Test feedback generation for good spec."""
        prompt = "Design a wooden table"
        spec = {
            "type": "table",
            "material": ["wood"],
            "dimensions": {"raw": "6 feet"},
            "purpose": "dining"
        }
        report = {
            "issues": [],
            "severity": "none",
            "quality_scores": {"completeness_score": 4}
        }
        
        feedback = generate_feedback(prompt, spec, report)
        
        # Good spec should have some feedback (even if suggesting improvements)
        assert "feedback_text" in feedback
        assert "actions" in feedback
        assert len(feedback["actions"]) > 0

class TestCompletenessScoring:
    """Test cases for completeness scoring."""
    
    def test_calculate_completeness_score_perfect(self):
        """Test completeness scoring for perfect spec."""
        spec = {
            "type": "table",
            "material": ["wood"],
            "color": "brown",
            "dimensions": {"raw": "6 feet"},
            "purpose": "dining"
        }
        
        score = calculate_completeness_score(spec)
        
        assert score == 10.0
    
    def test_calculate_completeness_score_partial(self):
        """Test completeness scoring for partial spec."""
        spec = {
            "type": "chair",
            "material": ["fabric"]
            # Missing color, dimensions, purpose
        }
        
        score = calculate_completeness_score(spec)
        
        assert 0 < score < 10
    
    def test_calculate_completeness_score_empty(self):
        """Test completeness scoring for empty spec."""
        spec = {}
        
        score = calculate_completeness_score(spec)
        
        assert score == 0

class TestEvaluatorEdgeCases:
    """Test edge cases and error conditions."""
    
    def test_evaluate_spec_with_none_values(self):
        """Test evaluation with None values."""
        prompt = "Design something"
        spec = {
            "type": None,
            "material": None,
            "dimensions": None,
            "purpose": None
        }
        
        report = evaluate_spec(prompt, spec)
        
        assert report["severity"] == "major"
        assert len(report["issues"]) > 0
    
    def test_evaluate_spec_with_empty_strings(self):
        """Test evaluation with empty strings."""
        prompt = "Create an object"
        spec = {
            "type": "",
            "material": [""],
            "dimensions": {"raw": ""},
            "purpose": ""
        }
        
        report = evaluate_spec(prompt, spec)
        
        assert report["severity"] in ["minor", "major"]
        assert len(report["issues"]) > 0
    
    def test_evaluate_spec_with_mixed_formats(self):
        """Test evaluation with mixed data formats."""
        prompt = "Build something"
        spec = {
            "type": "building",
            "material": "concrete",  # String instead of list
            "dimensions": "5 floors",  # String instead of dict
            "purpose": "office"
        }
        
        # Should handle mixed formats gracefully
        report = evaluate_spec(prompt, spec)
        
        assert isinstance(report, dict)
        assert "severity" in report
        assert "issues" in report

if __name__ == "__main__":
    pytest.main([__file__, "-v"])