import unittest
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from data_scorer import score_spec, parse_dimensions

class TestDataScorer(unittest.TestCase):
    
    def test_known_good_spec_high_score(self):
        """Test that a known good spec gets >= 8 score."""
        good_spec = {
            "type": "table",
            "material": "wood",
            "color": "brown",
            "dimensions": "6x4 feet",
            "purpose": "dining"
        }
        result = score_spec(good_spec, "Create a wooden dining table")
        self.assertGreaterEqual(result["format_score"], 8.0)
        self.assertEqual(result["completeness_score"], 4)
        self.assertEqual(result["material_realism_score"], 3)
    
    def test_incomplete_spec_low_score(self):
        """Test that incomplete spec gets lower score."""
        incomplete_spec = {
            "type": "unknown",
            "material": "unspecified",
            "color": "default",
            "dimensions": "standard",
            "purpose": "general"
        }
        result = score_spec(incomplete_spec, "Create furniture")
        self.assertLess(result["format_score"], 3.0)
        self.assertEqual(result["completeness_score"], 0)
    
    def test_dimension_parsing(self):
        """Test dimension parsing functionality."""
        # Test various dimension formats
        self.assertEqual(parse_dimensions("6x4 feet")["length_m"], 6 * 0.3048)
        self.assertEqual(parse_dimensions("2-floor")["floors"], 2)
        self.assertEqual(parse_dimensions("400 sqm")["area_m2"], 400.0)
        self.assertEqual(parse_dimensions("3 m")["size_m"], 3.0)
        self.assertEqual(parse_dimensions("standard"), {})

if __name__ == "__main__":
    unittest.main()