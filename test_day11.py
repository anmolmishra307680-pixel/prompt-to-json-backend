#!/usr/bin/env python3
"""
Test script for Day 11 CLI and web app functionality.
"""

import sys
import os
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent))

def test_cli_functionality():
    """Test enhanced CLI functionality."""
    print("=== Testing CLI Functionality ===")
    
    # Test basic pipeline
    from src.main import run_pipeline
    
    test_prompt = "Create a wooden table"
    print(f"Testing prompt: {test_prompt}")
    
    try:
        result = run_pipeline(test_prompt, save_report=False, run_rl=True)
        
        print(f"[PASS] Pipeline completed successfully")
        print(f"   Spec path: {result['spec_path']}")
        print(f"   Quality score: {result['scores']['format_score']}/10")
        print(f"   RL reward: {result['reward']:.3f}")
        print(f"   Issues: {len(result['evaluation']['issues'])}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] CLI test failed: {e}")
        return False

def test_web_app_imports():
    """Test web app imports and basic functionality."""
    print("\\n=== Testing Web App Imports ===")
    
    try:
        from src.web_app import main
        print("[PASS] Web app imports successfully")
        
        # Test that all required modules are available
        from src.main import run_pipeline
        from src.extractor import extract_basic_fields
        from utils import apply_fallbacks
        from data_scorer import score_spec
        from evaluator_agent import evaluate_spec
        
        print("[PASS] All required modules available")
        return True
        
    except ImportError as e:
        print(f"[FAIL] Web app import test failed: {e}")
        return False

def test_error_handling():
    """Test CLI error handling."""
    print("\\n=== Testing Error Handling ===")
    
    from src.main import run_pipeline
    
    # Test empty prompt (should generate low-quality spec)
    try:
        result = run_pipeline("", save_report=False, run_rl=False)
        if result['scores']['format_score'] < 5.0:  # Low quality expected
            print("[PASS] Empty prompt generates low-quality spec as expected")
        else:
            print("[FAIL] Empty prompt should generate low-quality spec")
            return False
    except Exception as e:
        print(f"[FAIL] Empty prompt handling failed: {e}")
        return False
    
    # Test very long prompt
    try:
        long_prompt = "Create a " + "very " * 50 + "long wooden table"
        result = run_pipeline(long_prompt, save_report=False, run_rl=False)
        print("[PASS] Long prompt handled successfully")
        return True
    except Exception as e:
        print(f"[FAIL] Long prompt failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Day 11 - CLI Polish + Streamlit Demo Tests")
    print("=" * 50)
    
    tests = [
        test_cli_functionality,
        test_web_app_imports,
        test_error_handling
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\\n=== Test Results ===")
    print(f"Passed: {passed}/{total}")
    
    if passed == total:
        print("[SUCCESS] All tests passed! Day 11 implementation is ready.")
        
        print("\\n=== Usage Instructions ===")
        print("CLI Usage:")
        print("  python src/main.py --prompt 'Create a wooden table'")
        print("  python src/main.py --prompt 'Design a chair' --save-report --run-rl")
        print("\\nWeb App Usage:")
        print("  streamlit run src/web_app.py")
        print("  Then open http://localhost:8501 in your browser")
        
    else:
        print("[FAIL] Some tests failed. Check the implementation.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)