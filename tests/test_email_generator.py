"""Tests for email generator."""

import pytest
from src.generators.email_generator import EmailGenerator

class TestEmailGenerator:
    
    def setup_method(self):
        self.generator = EmailGenerator()
    
    def test_basic_email_generation(self):
        """Test basic email generation with all required fields."""
        prompt = "Write an email to john@example.com about the meeting"
        result = self.generator.generate_spec(prompt)
        
        assert "spec" in result
        assert "llm_output" in result
        assert "method" in result
        
        spec = result["spec"]
        assert spec["type"] == "email"
        assert "to" in spec
        assert "subject" in spec
        assert "body" in spec
        assert "tone" in spec
    
    def test_email_recipient_extraction(self):
        """Test recipient extraction from prompt."""
        prompt = "Send email to marketing@company.com about project update"
        result = self.generator.generate_spec(prompt)
        
        spec = result["spec"]
        assert spec["to"] == "marketing@company.com"
    
    def test_email_subject_extraction(self):
        """Test subject extraction from prompt."""
        prompt = "Write email to team about quarterly meeting"
        result = self.generator.generate_spec(prompt)
        
        spec = result["spec"]
        assert "quarterly meeting" in spec["subject"].lower()
    
    def test_email_tone_detection(self):
        """Test tone detection from prompt."""
        formal_prompt = "Send a formal email to the board about results"
        result = self.generator.generate_spec(formal_prompt)
        assert result["spec"]["tone"] == "formal"
        
        casual_prompt = "Send a casual email to the team about lunch"
        result = self.generator.generate_spec(casual_prompt)
        assert result["spec"]["tone"] == "casual"
    
    def test_email_body_generation(self):
        """Test body content generation."""
        prompt = "Write email to team@company.com about project launch on October 1"
        result = self.generator.generate_spec(prompt)
        
        spec = result["spec"]
        body = spec["body"].lower()
        assert len(body) > 10
        assert "project launch" in body or "launch" in body
    
    def test_email_fallback_values(self):
        """Test fallback values for missing information."""
        prompt = "email"
        result = self.generator.generate_spec(prompt)
        
        spec = result["spec"]
        assert spec["to"] == "recipient@example.com"
        assert spec["subject"] == "Subject"
        assert spec["tone"] == "professional"
    
    def test_method_is_rules(self):
        """Test that method is set to rules."""
        prompt = "Write email to test@example.com"
        result = self.generator.generate_spec(prompt)
        assert result["method"] == "rules"