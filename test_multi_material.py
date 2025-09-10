"""Test multi-material extraction capabilities."""

from src.extractor import extract_basic_fields
from utils import apply_fallbacks

def test_multi_material():
    """Test extraction of multiple materials from complex prompts."""
    
    multi_material_prompts = [
        "Create a table with glass top and steel legs",
        "Design a cabinet with wooden frame and metal hardware", 
        "Build a chair with leather upholstery and aluminum base",
        "Make a drone with carbon fiber body and plastic propellers",
        "Construct a library with concrete foundation and glass walls"
    ]
    
    print("=== Multi-Material Extraction Test ===\n")
    
    for i, prompt in enumerate(multi_material_prompts, 1):
        print(f"Test {i}: {prompt}")
        
        extracted = extract_basic_fields(prompt)
        spec = apply_fallbacks(extracted)
        
        print(f"Materials detected: {extracted['material']}")
        print(f"Full spec: {spec}")
        print("-" * 60)

if __name__ == "__main__":
    test_multi_material()