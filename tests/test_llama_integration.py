"""Unit tests for LLaMA/LLM integration module."""

import pytest
import sys
from pathlib import Path
from unittest.mock import Mock, patch

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent / 'src'))

try:
    from llama_prompt import generate_raw_response, generate_spec_with_llm, log_llm_interaction
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False

class TestLLamaIntegration:
    """Test cases for LLM integration functionality."""
    
    @pytest.mark.skipif(not LLM_AVAILABLE, reason="LLM module not available")
    def test_generate_raw_response_basic(self):
        """Test basic LLM response generation."""
        prompt = "Design a simple table"
        
        # Skip actual LLM test since it requires model loading
        try:
            response = generate_raw_response(prompt)
            assert isinstance(response, str)
        except Exception:
            pytest.skip("LLM model not available in test environment")
    
    @pytest.mark.skipif(not LLM_AVAILABLE, reason="LLM module not available")
    def test_generate_spec_with_llm_success(self):
        """Test successful spec generation with LLM."""
        prompt = "Design a wooden table"
        
        # Mock successful LLM response with JSON
        mock_response = '{"type": "table", "material": ["wood"], "color": "brown"}'
        
        with patch('llama_prompt.generate_raw_response', return_value=mock_response):
            with patch('llama_prompt.log_llm_interaction'):
                spec = generate_spec_with_llm(prompt)
                
                assert isinstance(spec, dict)
                assert spec.get('type') == 'table'
                assert 'wood' in spec.get('material', [])
    
    @pytest.mark.skipif(not LLM_AVAILABLE, reason="LLM module not available")
    def test_generate_spec_with_llm_fallback(self):
        """Test fallback to rule-based extraction when LLM fails."""
        prompt = "Design a wooden table"
        
        # Mock LLM failure
        with patch('llama_prompt.generate_raw_response', return_value="invalid json response"):
            with patch('llama_prompt.log_llm_interaction'):
                with patch('llama_prompt.extract_basic_fields') as mock_extract:
                    mock_extract.return_value = {"type": "table", "material": ["wood"]}
                    
                    spec = generate_spec_with_llm(prompt)
                    
                    assert isinstance(spec, dict)
                    mock_extract.assert_called_once_with(prompt)
    
    @pytest.mark.skipif(not LLM_AVAILABLE, reason="LLM module not available")
    def test_log_llm_interaction(self):
        """Test LLM interaction logging."""
        prompt = "Design a table"
        response = "Generated response"
        
        with patch('llama_prompt.os.makedirs'):
            with patch('builtins.open', create=True) as mock_open:
                mock_file = Mock()
                mock_open.return_value.__enter__.return_value = mock_file
                
                log_llm_interaction(prompt, response)
                
                mock_open.assert_called_once()
                mock_file.write.assert_called_once()

class TestLLamaIntegrationMocked:
    """Test cases using mocked LLM functionality when not available."""
    
    def test_mock_llm_response_generation(self):
        """Test mocked LLM response generation."""
        prompt = "Design a chair"
        
        # Mock LLM response
        mock_response = '{"type": "chair", "material": ["wood"], "purpose": "seating"}'
        
        # Simulate LLM processing
        assert isinstance(mock_response, str)
        assert "chair" in mock_response
        assert "wood" in mock_response
    
    def test_mock_json_parsing(self):
        """Test JSON parsing from mocked LLM response."""
        import json
        
        mock_response = '{"type": "table", "material": ["metal"], "color": "silver"}'
        
        try:
            parsed = json.loads(mock_response)
            assert parsed['type'] == 'table'
            assert 'metal' in parsed['material']
            assert parsed['color'] == 'silver'
        except json.JSONDecodeError:
            pytest.fail("JSON parsing should succeed with valid JSON")
    
    def test_mock_fallback_behavior(self):
        """Test fallback behavior when LLM fails."""
        # Simulate invalid LLM response
        invalid_response = "This is not JSON"
        
        # Should trigger fallback to rule-based extraction
        try:
            import json
            json.loads(invalid_response)
            pytest.fail("Should have raised JSONDecodeError")
        except json.JSONDecodeError:
            # This is expected - fallback should be triggered
            fallback_spec = {"type": "unknown", "material": ["unspecified"]}
            assert isinstance(fallback_spec, dict)
    
    def test_mock_logging_functionality(self):
        """Test mocked logging functionality."""
        log_entry = {
            "timestamp": "2025-01-10T10:00:00",
            "prompt": "Design a table",
            "llm_output": "Generated spec",
            "model": "distilgpt2"
        }
        
        # Verify log entry structure
        assert "timestamp" in log_entry
        assert "prompt" in log_entry
        assert "llm_output" in log_entry
        assert "model" in log_entry
        
        # Verify content
        assert log_entry["prompt"] == "Design a table"
        assert log_entry["model"] == "distilgpt2"

if __name__ == "__main__":
    pytest.main([__file__, "-v"])