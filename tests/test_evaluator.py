import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from evaluator_agent import evaluate_spec

class TestEvaluator(unittest.TestCase):
    
    def test_missing_dimensions(self):
        """Test that missing dimensions are detected."""
        spec = {
            "type": "table",
            "material": "wood",
            "color": "brown",
            "dimensions": "standard",
            "purpose": "dining"
        }
        result = evaluate_spec("Create a dining table", spec)
        self.assertIn("dimensions_missing", result["issues"])
    
    def test_missing_material(self):
        """Test that missing material is detected."""
        spec = {
            "type": "chair",
            "material": "unspecified",
            "color": "black",
            "dimensions": "2x2 feet",
            "purpose": "office"
        }
        result = evaluate_spec("Create an office chair", spec)
        self.assertIn("material_missing", result["issues"])
    
    def test_complete_spec(self):
        """Test that complete spec has no issues."""
        spec = {
            "type": "table",
            "material": "wood",
            "color": "brown",
            "dimensions": "6 feet",
            "purpose": "dining"
        }
        result = evaluate_spec("Create a wooden dining table", spec)
        self.assertEqual(len(result["issues"]), 0)
        self.assertEqual(result["severity"], "none")

if __name__ == "__main__":
    unittest.main()