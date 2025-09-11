"""Smoke tests for Streamlit integration."""

import pytest
import sys
from unittest.mock import patch, MagicMock

class TestStreamlitIntegration:
    
    def test_web_app_imports(self):
        """Test that web app imports work correctly."""
        try:
            from src.web_app import main
            assert callable(main)
        except ImportError as e:
            pytest.fail(f"Web app import failed: {e}")
    
    @patch('streamlit.set_page_config')
    @patch('streamlit.title')
    @patch('streamlit.markdown')
    @patch('streamlit.header')
    @patch('streamlit.text_area')
    @patch('streamlit.columns')
    @patch('streamlit.button')
    def test_web_app_basic_structure(self, mock_button, mock_columns, mock_text_area, 
                                   mock_header, mock_markdown, mock_title, mock_config):
        """Test basic web app structure without running Streamlit."""
        
        # Mock streamlit components
        mock_columns.return_value = [MagicMock(), MagicMock()]
        mock_text_area.return_value = ""
        mock_button.return_value = False
        
        # Mock session state
        with patch('streamlit.session_state', {}):
            try:
                from src.web_app import main
                # Don't actually call main() as it would start Streamlit
                # Just verify the function exists and imports work
                assert callable(main)
            except Exception as e:
                pytest.fail(f"Web app structure test failed: {e}")
    
    def test_classifier_integration(self):
        """Test classifier integration in web app context."""
        from src.classifier import classify_prompt
        
        # Test email classification
        email_result = classify_prompt("Write email to team about meeting")
        assert email_result["type"] == "email"
        assert email_result["confidence"] > 0.5
        
        # Test design classification
        design_result = classify_prompt("Create a wooden table")
        assert design_result["type"] == "design"
        assert design_result["confidence"] > 0.5
    
    def test_generator_integration(self):
        """Test generator integration in web app context."""
        from src.generators import EmailGenerator, DesignGenerator
        
        # Test email generator
        email_gen = EmailGenerator()
        email_result = email_gen.generate_spec("Write email to test@example.com")
        assert email_result["spec"]["type"] == "email"
        
        # Test design generator
        design_gen = DesignGenerator()
        design_result = design_gen.generate_spec("Create a wooden table")
        assert design_result["spec"]["type"] == "table"
    
    def test_schema_registry_integration(self):
        """Test schema registry integration in web app context."""
        from src.schema_registry import get_schema_for_type, validate_spec
        
        # Test getting schema info
        email_schema = get_schema_for_type("email")
        assert email_schema["type"] == "email"
        assert len(email_schema["examples"]) > 0
        
        # Test validation
        test_spec = {
            "type": "email",
            "to": "test@example.com",
            "subject": "Test",
            "body": "Test content"
        }
        validation = validate_spec(test_spec, "email")
        assert validation["valid"] is True
    
    def test_evaluator_integration(self):
        """Test evaluator integration in web app context."""
        from src.evaluators import EmailEvaluator, DesignEvaluator
        
        # Test email evaluator
        email_eval = EmailEvaluator()
        email_spec = {
            "type": "email",
            "to": "test@example.com",
            "subject": "Test Subject",
            "body": "Test body content",
            "tone": "professional"
        }
        email_result = email_eval.evaluate("Write email to test@example.com", email_spec)
        assert "critic_feedback" in email_result
        assert "scores" in email_result
        
        # Test design evaluator
        design_eval = DesignEvaluator()
        design_spec = {
            "type": "table",
            "material": ["wood"],
            "color": "brown",
            "dimensions": {"raw": "6 feet"},
            "purpose": "dining"
        }
        design_result = design_eval.evaluate("Create a wooden dining table", design_spec)
        assert "critic_feedback" in design_result
        assert "scores" in design_result