import pytest
import json
import os
from src.llama_prompt import refine_with_llm

def test_refine_with_llm_structure():
    """Test that refine_with_llm returns expected structure"""
    result = refine_with_llm("Create a red gearbox with steel gears.")
    
    assert "prompt" in result
    assert "extractor_output" in result
    assert "llm_raw" in result
    assert "timestamp" in result
    
    # Check extractor output structure
    extractor = result["extractor_output"]
    assert extractor["type"] == "gearbox"
    assert "steel" in extractor["material"]
    assert extractor["color"] == "red"

def test_logging_functionality():
    """Test that entries are logged to data/logs.json"""
    # Clear logs for clean test
    log_file = "data/logs.json"
    if os.path.exists(log_file):
        with open(log_file, 'w') as f:
            json.dump([], f)
    
    # Run function
    refine_with_llm("Test prompt for logging")
    
    # Check log was created
    assert os.path.exists(log_file)
    with open(log_file, 'r') as f:
        logs = json.load(f)
    
    assert len(logs) >= 1
    assert logs[-1]["prompt"] == "Test prompt for logging"