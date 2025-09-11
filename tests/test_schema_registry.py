"""Tests for schema registry functionality."""

import pytest
import json
from src.schema_registry import (
    get_schema_for_type, 
    get_available_types, 
    validate_spec, 
    save_valid_spec,
    get_examples_for_type
)

class TestSchemaRegistry:
    
    def test_get_available_types(self):
        """Test getting list of available types."""
        types = get_available_types()
        assert isinstance(types, list)
        assert "design" in types
        assert "email" in types
        assert "unknown" in types
    
    def test_get_schema_for_design(self):
        """Test getting schema for design type."""
        schema_info = get_schema_for_type("design")
        
        assert schema_info["type"] == "design"
        assert "examples" in schema_info
        assert "help" in schema_info
        assert "schema" in schema_info
        
        # Check schema structure
        if schema_info["schema"]:
            assert "type" in schema_info["schema"]
            assert "properties" in schema_info["schema"]
    
    def test_get_schema_for_email(self):
        """Test getting schema for email type."""
        schema_info = get_schema_for_type("email")
        
        assert schema_info["type"] == "email"
        assert len(schema_info["examples"]) > 0
        assert "email" in schema_info["help"].lower()
        
        # Check email schema properties
        if schema_info["schema"]:
            props = schema_info["schema"]["properties"]
            assert "to" in props
            assert "subject" in props
            assert "body" in props
    
    def test_get_schema_for_unknown_type(self):
        """Test getting schema for unknown type."""
        schema_info = get_schema_for_type("nonexistent")
        assert schema_info["type"] == "unknown"
    
    def test_validate_valid_email_spec(self):
        """Test validation of valid email specification."""
        valid_email_spec = {
            "type": "email",
            "to": "test@example.com",
            "subject": "Test Subject",
            "body": "Test body content"
        }
        
        result = validate_spec(valid_email_spec, "email")
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_validate_invalid_email_spec(self):
        """Test validation of invalid email specification."""
        invalid_email_spec = {
            "type": "email",
            "to": "test@example.com"
            # Missing required subject and body
        }
        
        result = validate_spec(invalid_email_spec, "email")
        assert result["valid"] is False
        assert len(result["errors"]) > 0
    
    def test_validate_design_spec(self):
        """Test validation of design specification."""
        design_spec = {
            "type": "table",
            "material": ["wood"],
            "color": "brown"
        }
        
        result = validate_spec(design_spec, "design")
        assert result["valid"] is True
    
    def test_validate_unknown_type(self):
        """Test validation of unknown type (should pass)."""
        spec = {"type": "unknown", "data": "test"}
        result = validate_spec(spec, "unknown")
        assert result["valid"] is True
    
    def test_get_examples_for_type(self):
        """Test getting examples for different types."""
        email_examples = get_examples_for_type("email")
        assert isinstance(email_examples, list)
        assert len(email_examples) > 0
        assert any("email" in ex.lower() for ex in email_examples)
        
        design_examples = get_examples_for_type("design")
        assert isinstance(design_examples, list)
        assert len(design_examples) > 0
    
    def test_save_valid_spec(self):
        """Test saving valid specification."""
        spec = {
            "type": "email",
            "to": "test@example.com",
            "subject": "Test",
            "body": "Test content"
        }
        
        filepath = save_valid_spec(spec, "email")
        assert filepath is not None
        assert "email" in filepath
        assert filepath.endswith(".json")
        
        # Verify file was created and contains correct data
        with open(filepath, 'r') as f:
            saved_spec = json.load(f)
        
        assert saved_spec["type"] == "email"
        assert saved_spec["to"] == "test@example.com"