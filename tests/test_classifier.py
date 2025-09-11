"""Tests for prompt classifier."""

import pytest
from src.classifier import classify_prompt, classify_prompt_rules, get_classification_suggestions

class TestClassifyPromptRules:
    """Test rule-based classification."""
    
    def test_email_classification(self):
        """Test email prompt classification."""
        prompt = "Please write a short professional email to the marketing team"
        result = classify_prompt_rules(prompt)
        
        assert result[0] == "email"
        assert result[1] > 0.5  # Good confidence
        assert "email" in result[2].lower()
    
    def test_design_classification(self):
        """Test design prompt classification."""
        prompt = "Create a wooden dining table with glass top"
        result = classify_prompt_rules(prompt)
        
        assert result[0] == "design"
        assert result[1] > 0.5
        assert "create" in result[2].lower() or "table" in result[2].lower()
    
    def test_code_classification(self):
        """Test code prompt classification."""
        prompt = "Write a Python function to sort a list"
        result = classify_prompt_rules(prompt)
        
        assert result[0] == "code"
        assert result[1] > 0.5
        assert "python" in result[2].lower() or "function" in result[2].lower()
    
    def test_document_classification(self):
        """Test document prompt classification."""
        prompt = "Write a business report about quarterly sales"
        result = classify_prompt_rules(prompt)
        
        assert result[0] == "document"
        assert result[1] > 0.5
        assert "report" in result[2].lower()
    
    def test_unknown_classification(self):
        """Test unknown prompt classification."""
        prompt = "Hello world how are you today"
        result = classify_prompt_rules(prompt)
        
        assert result[0] == "unknown"
        assert result[1] == 0.0
        assert "no rule matches" in result[2]

class TestClassifyPrompt:
    """Test main classification function."""
    
    def test_email_prompt_full(self):
        """Test full email classification."""
        prompt = "Please write a short professional email to the marketing team announcing the new project launch"
        result = classify_prompt(prompt)
        
        assert result["type"] == "email"
        assert result["confidence"] > 0.6
        assert "email" in result["reason"].lower()
    
    def test_design_prompt_full(self):
        """Test full design classification."""
        prompt = "Create a wooden dining table"
        result = classify_prompt(prompt)
        
        assert result["type"] == "design"
        assert result["confidence"] > 0.6
        assert ("create" in result["reason"].lower() or "table" in result["reason"].lower())
    
    def test_furniture_variations(self):
        """Test various furniture prompts."""
        furniture_prompts = [
            "Design a modern steel chair",
            "Build a glass desk for office",
            "Make a red leather sofa",
            "Construct a wooden cabinet"
        ]
        
        for prompt in furniture_prompts:
            result = classify_prompt(prompt)
            assert result["type"] == "design"
            assert result["confidence"] > 0.3  # Lower threshold for edge cases
    
    def test_email_variations(self):
        """Test various email prompts."""
        email_prompts = [
            "Send an email to the team",
            "Compose a message for the client",
            "Write an email with subject line",
            "Draft a professional email"
        ]
        
        for prompt in email_prompts:
            result = classify_prompt(prompt)
            assert result["type"] == "email"
            assert result["confidence"] > 0.5
    
    def test_empty_prompt(self):
        """Test empty prompt handling."""
        result = classify_prompt("")
        
        assert result["type"] == "unknown"
        assert result["confidence"] == 0.0
        assert "empty prompt" in result["reason"]
    
    def test_none_prompt(self):
        """Test None prompt handling."""
        result = classify_prompt(None)
        
        assert result["type"] == "unknown"
        assert result["confidence"] == 0.0
        assert "empty prompt" in result["reason"]

class TestClassificationSuggestions:
    """Test classification suggestions."""
    
    def test_email_suggestions(self):
        """Test email suggestions."""
        suggestions = get_classification_suggestions("email")
        
        assert len(suggestions) >= 2
        assert any("email" in s.lower() for s in suggestions)
        assert any("furniture" in s.lower() or "design" in s.lower() for s in suggestions)
    
    def test_design_suggestions(self):
        """Test design suggestions."""
        suggestions = get_classification_suggestions("design")
        
        assert len(suggestions) >= 2
        assert any("design" in s.lower() or "furniture" in s.lower() for s in suggestions)
    
    def test_unknown_suggestions(self):
        """Test unknown suggestions."""
        suggestions = get_classification_suggestions("unknown")
        
        assert len(suggestions) >= 2
        assert any("furniture" in s.lower() or "design" in s.lower() for s in suggestions)

class TestEdgeCases:
    """Test edge cases and complex prompts."""
    
    def test_mixed_keywords(self):
        """Test prompt with mixed keywords."""
        prompt = "Create a design document for the email marketing table"
        result = classify_prompt(prompt)
        
        # Should classify based on strongest signal
        assert result["type"] in ["design", "document", "email"]
        assert result["confidence"] > 0.0
    
    def test_long_prompt(self):
        """Test very long prompt."""
        prompt = "I need you to help me create a beautiful wooden dining table " * 10
        result = classify_prompt(prompt)
        
        assert result["type"] == "design"
        assert result["confidence"] > 0.5
    
    def test_case_insensitive(self):
        """Test case insensitive matching."""
        prompts = [
            "CREATE A WOODEN TABLE",
            "create a wooden table",
            "Create A Wooden Table"
        ]
        
        for prompt in prompts:
            result = classify_prompt(prompt)
            assert result["type"] == "design"
    
    def test_special_characters(self):
        """Test prompts with special characters."""
        prompt = "Create a wooden table!!! @#$%"
        result = classify_prompt(prompt)
        
        assert result["type"] == "design"
        assert result["confidence"] > 0.5

class TestIntegration:
    """Integration tests with realistic scenarios."""
    
    def test_realistic_email_prompt(self):
        """Test realistic email prompt."""
        prompt = "Please write a short, professional email to the marketing team announcing the new project launch. Make sure to include the launch date of October 1st. Keep it concise."
        result = classify_prompt(prompt)
        
        assert result["type"] == "email"
        assert result["confidence"] >= 0.8
        assert "email" in result["reason"].lower()
    
    def test_realistic_furniture_prompt(self):
        """Test realistic furniture prompt."""
        prompt = "Design a modern minimalist dining table made of oak wood with steel legs, suitable for a family of 4"
        result = classify_prompt(prompt)
        
        assert result["type"] == "design"
        assert result["confidence"] >= 0.8
    
    def test_ambiguous_prompt(self):
        """Test ambiguous prompt."""
        prompt = "Help me with something"
        result = classify_prompt(prompt)
        
        # Should handle gracefully
        assert result["type"] in ["unknown", "email", "design", "code", "document"]
        assert 0.0 <= result["confidence"] <= 1.0

if __name__ == "__main__":
    pytest.main([__file__, "-v"])